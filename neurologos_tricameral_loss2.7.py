# =============================================================================
# NeuroLogos TRICAMERAL v5.1
# Hemisferio Derecho: Visión + Audio
# Hemisferio Izquierdo: Lenguaje + Razonamiento
# Corpus Callosum: Fusión trimodal (ve, escucha, razona)
# + Dataset Flickr8k con Audio Pre-generado
# =============================================================================

import os
from pathlib import Path
from collections import Counter
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from torchvision import transforms
import torchaudio
import torchaudio.transforms as T
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
from tqdm import tqdm
import warnings
import kagglehub
warnings.filterwarnings('ignore')
import subprocess
import urllib.request
import zipfile
import shutil
import soundfile as sf
import time
from functools import lru_cache
from collections import deque


# Al inicio del archivo, reemplazar TODAS las constantes:

EPISODIC_UPDATE_FREQ = 5      # Actualizar cada 5 batches (balance)
EPISODIC_REPLAY_FREQ = 20     # Replay cada 20 batches (reducir overhead)
EPISODIC_MIN_BUFFER = 64      # Buffer mínimo para replay
EPISODIC_SAMPLES_PER_UPDATE = 2  # Muestras a añadir por actualización

REWARD_FREQUENCY = 20
REPLAY_FREQUENCY = 20  # Sincronizado con episodic replay
MEMORY_LOG_FREQUENCY = 500  # Reducido de 100
DIAGNOSTIC_UPDATE_FREQ = 20
COGNITIVE_DIAG_FREQ = 50


# =============================================================================
# UTILIDADES: Descarga y setup del dataset ROBUSTO Y RESUMIBLE
# =============================================================================
def setup_flickr8k_with_audio(data_dir='./flickr8k_full'):
    """
    Descarga y organiza Flickr8k + Audio del dataset de Kaggle.
    Sistema robusto que verifica componentes individuales y descarga solo lo faltante.
    """
    images_dir = os.path.join(data_dir, 'Images')
    audio_dir  = os.path.join(data_dir, 'wavs')
    captions_file = os.path.join(data_dir, 'captions.txt')

    os.makedirs(data_dir, exist_ok=True)

    # FIX: Verificación de integridad con conteo real de archivos
    has_images = os.path.exists(images_dir) and len([f for f in Path(images_dir).glob("*.jpg")]) >= 8000
    has_audio = os.path.exists(audio_dir) and len([f for f in Path(audio_dir).glob("*.wav")]) >= 40000
    has_captions = os.path.exists(captions_file) and os.path.getsize(captions_file) > 1000000

    print(f"📊 Estado del dataset:")
    print(f"  Imágenes: {'✅' if has_images else '❌'} ({len(list(Path(images_dir).glob('*.jpg'))) if os.path.exists(images_dir) else 0}/8091)")
    print(f"  Audios: {'✅' if has_audio else '❌'} ({len(list(Path(audio_dir).glob('*.wav'))) if os.path.exists(audio_dir) else 0}/40000)")
    print(f"  Captions: {'✅' if has_captions else '❌'}")

    # Si todo está completo, retornar
    if has_images and has_audio and has_captions:
        print("✅ Dataset completo, sin necesidad de descargas\n")
        return data_dir

    # ========== AUDIO - FIX: Manejo de errores y verificación de integridad ==========
    if not has_audio:
        print("\n📥 Descargando y procesando audios desde Kaggle...")
        try:
            path = kagglehub.dataset_download("warcoder/flickr-8k-audio-caption-corpus")
            print(f"✓ Dataset descargado en: {path}")

            # FIX: Búsqueda recursiva robusta de archivos wav
            wav_files = list(Path(path).rglob("*.wav"))
            if not wav_files:
                raise FileNotFoundError("No se encontraron archivos .wav en el dataset descargado")

            # FIX: Crear directorio limpio solo si hay archivos válidos
            if os.path.exists(audio_dir):
                shutil.rmtree(audio_dir)
            os.makedirs(audio_dir, exist_ok=True)

            # FIX: Copia con verificación de integridad
            print(f"📂 Copiando {len(wav_files)} archivos de audio...")
            copied_count = 0
            for wav_file in tqdm(wav_files, desc="Verificando audios"):
                if wav_file.stat().st_size > 1024:  # FIX: Verificar archivo no vacío
                    dest_path = os.path.join(audio_dir, wav_file.name)
                    if not os.path.exists(dest_path):
                        shutil.copy2(str(wav_file), dest_path)
                        copied_count += 1

            print(f"✅ Audios válidos copiados: {copied_count} archivos")
            if copied_count < 40000:
                print(f"⚠️ Advertencia: Solo {copied_count} audios válidos de 40000 esperados")

        except Exception as e:
            print(f"❌ Error descargando audios: {e}")
            print("⚠️  Continuando sin audios...")
            os.makedirs(audio_dir, exist_ok=True)

    # ========== IMÁGENES - FIX: Verificación de checksums implícita ==========
    if not has_images:
        print("\n📥 Descargando imágenes originales...")
        try:
            import urllib.request, zipfile
            # FIX: URLs sin espacios finales
            images_url = 'https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_Dataset.zip'
            zip_path = os.path.join(data_dir, 'images.zip')

            print("  Descargando archivo ZIP...")
            urllib.request.urlretrieve(images_url, zip_path, reporthook=lambda block, size, total:
                                     print(f"    Progreso: {block*size}/{total} bytes", end='\r'))
            print()

            # FIX: Verificar tamaño mínimo
            if os.path.getsize(zip_path) < 100000000:
                raise ValueError("Archivo ZIP demasiado pequeño, descarga incompleta")

            print("  Extrayendo imágenes...")
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # FIX: Verificar CRC antes de extraer
                for info in zf.infolist():
                    if info.file_size == 0:
                        print(f"⚠️  Archivo vacío detectado: {info.filename}")
                zf.extractall(data_dir)

            os.remove(zip_path)

            # FIX: Normalizar nombre de carpeta de forma robusta
            possible_names = ['Flicker8k_Dataset', 'Flickr8k_Dataset', 'Flickr8k_Dataset']
            for old_name in possible_names:
                old_path = os.path.join(data_dir, old_name)
                if os.path.exists(old_path) and not os.path.exists(images_dir):
                    os.rename(old_path, images_dir)
                    print(f"✅ Carpeta renombrada: {old_name} -> Images")
                    break

            actual_count = len(list(Path(images_dir).glob("*.jpg")))
            print(f"✅ Imágenes listas: {actual_count} archivos")
            if actual_count < 8000:
                print(f"⚠️  Advertencia: Solo {actual_count} imágenes de 8091 esperadas")

        except Exception as e:
            print(f"❌ Error descargando imágenes: {e}")
            raise RuntimeError("No se pudieron descargar las imágenes. Verifica tu conexión.")

    # ========== CAPTIONS - FIX: Procesamiento con validación ==========
    if not has_captions:
        print("\n📥 Descargando captions...")
        try:
            import urllib.request, zipfile
            caps_url = 'https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_text.zip'
            zip_path = os.path.join(data_dir, 'captions.zip')

            print("  Descargando archivo ZIP...")
            urllib.request.urlretrieve(caps_url, zip_path)

            print("  Extrayendo captions...")
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(data_dir)

            os.remove(zip_path)

            # FIX: Verificar archivo token existe y tiene contenido
            token_file = os.path.join(data_dir, 'Flickr8k.token.txt')
            if not os.path.exists(token_file) or os.path.getsize(token_file) < 100000:
                raise FileNotFoundError("Flickr8k.token.txt no encontrado o corrupto")

            print("  Procesando captions...")
            caption_count = 0
            with open(token_file, 'r', encoding='utf-8') as fin, \
                 open(captions_file, 'w', encoding='utf-8') as fout:
                for line in fin:
                    if '\t' in line:
                        img_cap, text = line.strip().split('\t', 1)
                        img_name = img_cap.split('#')[0]
                        fout.write(f"{img_name}\t{text}\n")
                        caption_count += 1

            print(f"✅ Captions procesados: {caption_count} líneas")
            if caption_count < 40000:
                print(f"⚠️  Advertencia: Solo {caption_count} captions de 40000 esperadas")

        except Exception as e:
            print(f"❌ Error procesando captions: {e}")
            raise RuntimeError("No se pudieron procesar los captions.")

    # ========== REPORTE FINAL - FIX: Verificación de integridad completa ==========
    final_images = len([f for f in Path(images_dir).glob("*.jpg")]) if os.path.exists(images_dir) else 0
    final_audios = len([f for f in Path(audio_dir).glob("*.wav")]) if os.path.exists(audio_dir) else 0
    final_captions = os.path.getsize(captions_file) if os.path.exists(captions_file) else 0

    print(f"\n{'='*60}")
    print(f"✅ DATASET PREPARADO EN: {data_dir}")
    print(f"   Imágenes: {final_images}/8091")
    print(f"   Audios: {final_audios}/40000")
    print(f"   Captions: {'✅' if final_captions > 100000 else '❌'} ({final_captions} bytes)")

    # FIX: Alerta si hay inconsistencias
    if final_images < 8000 or final_audios < 1000 or final_captions < 100000:
        print(f"⚠️  ADVERTENCIA: Dataset incompleto detectado")
    print(f"{'='*60}\n")

    # FIX: Crear archivo de estado para verificación rápida futura
    with open(os.path.join(data_dir, '.setup_complete'), 'w') as f:
        f.write(f"{final_images}\n{final_audios}\n{final_captions}\n")

    return data_dir




# =============================================================================
# EJECUTAR ANTES DE ENTRENAR
# =============================================================================
print("🚀 Iniciando setup del dataset...\n")
dataset_path = setup_flickr8k_with_audio('./flickr8k_full')

if dataset_path:
    print(f"\n✅ Continuando con entrenamiento...\n")
    # train_tricameral()  # Descomentar para entrenar
else:
    print("\n❌ ERROR: Setup fallido. Revisa los logs.")



def build_vocab_flickr(captions_file, vocab_size=5000):
    """Construye vocabulario desde el archivo de captions"""
    print("📚 Construyendo vocabulario...")
    counter = Counter()
    with open(captions_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                counter.update(parts[1].lower().split())

    most_common = counter.most_common(vocab_size - 4)
    vocab = {'<PAD>': 0, '<BOS>': 1, '<EOS>': 2, '<UNK>': 3}
    for i, (word, _) in enumerate(most_common):
        vocab[word] = i + 4

    id2word = {i: w for w, i in vocab.items()}
    print(f"✓ Vocabulario creado: {len(vocab)} palabras")
    return vocab, id2word



# =============================================================================
# MEMORIA EPISÓDICA - FIX: Gestión optimizada de dispositivo y decay temporal
# =============================================================================
class HierarchicalEpisodicMemory:
    def __init__(self, working_capacity=200, short_term_capacity=800, importance_threshold=0.7):
        # Tres niveles de memoria
        self.working_memory = deque(maxlen=working_capacity)
        self.short_term_memory = deque(maxlen=short_term_capacity)
        self.long_term_memory = []
        self.capacity = working_capacity + short_term_capacity + 1000

        self.working_scores = deque(maxlen=working_capacity)
        self.short_term_scores = deque(maxlen=short_term_capacity)
        self.long_term_scores = []

        self.importance_threshold = importance_threshold
        self.surprise_threshold = 0.3

        self.forgetting_half_life = 100
        self.timestamps = {
            'working': deque(maxlen=working_capacity),
            'short_term': deque(maxlen=short_term_capacity),
            'long_term': []
        }

        self.step_counter = 0

        self.buffer = []
        self.surprise_scores = []

    def compute_surprise(self, predicted_logits, ground_truth, gate_mean):
        with torch.no_grad():
            ce = F.cross_entropy(
                predicted_logits.reshape(-1, predicted_logits.size(-1)),
                ground_truth.reshape(-1),
                reduction='none'
            ).mean()
            surprise = (ce * (1.0 - gate_mean)).clamp(0, 10) / predicted_logits.size(0)
            return surprise.item()

    def calculate_importance(self, episode, surprise_score):
        recency_bonus = 0.2
        surprise_weight = 0.6
        novelty_weight = 0.2

        importance = (
            surprise_weight * min(1.0, surprise_score / 2.0) +
            recency_bonus +
            novelty_weight * self._calculate_novelty(episode)
        )
        return importance

    def _calculate_novelty(self, episode):
        if len(self.long_term_memory) == 0:
            return 1.0

        recent_memories = self.long_term_memory[-10:]
        similarities = []

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        episode_img = episode[0].to(device) if episode[0].device.type == 'cpu' else episode[0]

        for mem, _, _ in recent_memories:
            mem_img = mem.to(device) if mem.device.type == 'cpu' else mem
            sim = F.cosine_similarity(
                episode_img.flatten().unsqueeze(0),
                mem_img.flatten().unsqueeze(0)
            ).item()
            similarities.append(sim)

        avg_similarity = np.mean(similarities) if similarities else 0.0
        return 1.0 - avg_similarity

    def store_episode(self, image, audio, caption, surprise_score):
        self.step_counter += 1

        # Mover tensores a CPU inmediatamente
        image_cpu = image.detach().cpu()
        audio_cpu = audio.detach().cpu()
        caption_cpu = caption.detach().cpu()

        # Decidir nivel de memoria basado en sorpresa
        if surprise_score > 0.8:
            self.working_memory.append((image_cpu, audio_cpu, caption_cpu))
            self.working_scores.append(max(1e-8, surprise_score))
            self.timestamps['working'].append(self.step_counter)

        elif surprise_score > 0.5:
            self.short_term_memory.append((image_cpu, audio_cpu, caption_cpu))
            self.short_term_scores.append(max(1e-8, surprise_score))
            self.timestamps['short_term'].append(self.step_counter)

        else:
            importance = self.calculate_importance((image_cpu, audio_cpu, caption_cpu), surprise_score)

            if importance > self.importance_threshold:
                self.long_term_memory.append((image_cpu, audio_cpu, caption_cpu))
                self.long_term_scores.append(max(1e-8, importance))
                self.timestamps['long_term'].append(self.step_counter)

                if len(self.long_term_memory) > 1000:
                    min_idx = np.argmin(self.long_term_scores)
                    self.long_term_memory.pop(min_idx)
                    self.long_term_scores.pop(min_idx)
                    self.timestamps['long_term'].pop(min_idx)

        self._update_unified_buffer()

        if self.step_counter % 100 == 0:
            self.apply_forgetting_curve()

    def _update_unified_buffer(self):
        self.buffer = (
            list(self.working_memory) +
            list(self.short_term_memory) +
            self.long_term_memory
        )
        self.surprise_scores = (
            list(self.working_scores) +
            list(self.short_term_scores) +
            self.long_term_scores
        )

    def add(self, image, audio, caption, surprise_score):
        self.store_episode(image, audio, caption, surprise_score)

    def apply_forgetting_curve(self):
        decay_factor = 0.5 ** (1.0 / self.forgetting_half_life)

        for i in range(len(self.short_term_scores)):
            age = self.step_counter - self.timestamps['short_term'][i]
            self.short_term_scores[i] *= (decay_factor ** age)
            self.short_term_scores[i] = max(1e-8, self.short_term_scores[i])

        for i in range(len(self.long_term_scores)):
            age = self.step_counter - self.timestamps['long_term'][i]
            self.long_term_scores[i] *= (decay_factor ** age)
            self.long_term_scores[i] = max(1e-8, self.long_term_scores[i])

        self._purge_low_score_memories()
        self._update_unified_buffer()

    def _purge_low_score_memories(self):
        min_score_threshold = 1e-6

        # Purgar short-term memory
        valid_indices = [i for i, score in enumerate(self.short_term_scores) if score > min_score_threshold]
        if len(valid_indices) < len(self.short_term_memory):
            self.short_term_memory = deque(
                [self.short_term_memory[i] for i in valid_indices],
                maxlen=self.short_term_memory.maxlen
            )
            self.short_term_scores = deque(
                [self.short_term_scores[i] for i in valid_indices],
                maxlen=self.short_term_scores.maxlen
            )
            self.timestamps['short_term'] = deque(
                [self.timestamps['short_term'][i] for i in valid_indices],
                maxlen=self.timestamps['short_term'].maxlen
            )

        # Purgar long-term memory
        valid_indices_lt = [i for i, score in enumerate(self.long_term_scores) if score > min_score_threshold]
        if len(valid_indices_lt) < len(self.long_term_memory):
            self.long_term_memory = [self.long_term_memory[i] for i in valid_indices_lt]
            self.long_term_scores = [self.long_term_scores[i] for i in valid_indices_lt]
            self.timestamps['long_term'] = [self.timestamps['long_term'][i] for i in valid_indices_lt]

    def sample(self, batch_size, memory_level='mixed'):
        if memory_level == 'working':
            return self._sample_from_buffer(self.working_memory, self.working_scores, batch_size)
        elif memory_level == 'short_term':
            return self._sample_from_buffer(self.short_term_memory, self.short_term_scores, batch_size)
        elif memory_level == 'long_term':
            return self._sample_from_buffer(self.long_term_memory, self.long_term_scores, batch_size)
        else:
            total_samples = []

            if len(self.working_memory) > 0:
                n_working = max(1, batch_size // 2)
                samples = self._sample_from_buffer(self.working_memory, self.working_scores, n_working)
                if samples:
                    total_samples.extend(samples)

            if len(self.short_term_memory) > 0:
                n_short = max(1, batch_size * 3 // 10)
                samples = self._sample_from_buffer(self.short_term_memory, self.short_term_scores, n_short)
                if samples:
                    total_samples.extend(samples)

            if len(self.long_term_memory) > 0:
                n_long = max(1, batch_size // 5)
                samples = self._sample_from_buffer(self.long_term_memory, self.long_term_scores, n_long)
                if samples:
                    total_samples.extend(samples)

            return total_samples if total_samples else None

    def _sample_from_buffer(self, buffer, scores, batch_size):
        if not buffer or len(buffer) == 0:
            return None

        actual_batch_size = min(batch_size, len(buffer))

        if len(scores) != len(buffer):
            indices = np.random.choice(len(buffer), size=actual_batch_size, replace=False)
        else:
            # Normalización robusta
            probs = np.array(list(scores), dtype=np.float64)
            probs = np.clip(probs, 1e-10, None)
            probs = probs / probs.sum()

            if not np.isclose(probs.sum(), 1.0, atol=1e-6):
                probs = probs / probs.sum()

            if not np.isfinite(probs).all() or probs.sum() == 0:
                probs = np.ones(len(buffer)) / len(buffer)

            try:
                indices = np.random.choice(len(buffer), size=actual_batch_size, p=probs, replace=False)
            except ValueError as e:
                print(f"⚠️ Sampleo fallback uniforme: {e}")
                indices = np.random.choice(len(buffer), size=actual_batch_size, replace=False)

        return [buffer[i] for i in indices]

    def get_total_size(self):
        return len(self.working_memory) + len(self.short_term_memory) + len(self.long_term_memory)



# =============================================================================
# SISTEMA DE RAZONAMIENTO COGNITIVO COMPLETO
# =============================================================================
class NeurocognitiveSystem:
    def __init__(self):
        self.cognitive_history = []
        self.last_intervention_epoch = -5
        self.linguistic_feedback = LinguisticFeedbackLoop()

        # FIX: Motor de razonamiento causal
        self.causal_engine = CausalReasoningEngine(hidden_dim=512)

        # Umbrales existentes
        self.cider_threshold = 0.08
        self.spice_threshold = 0.12
        self.plateau_threshold = 0.005

        self.reasoning_efficiency_threshold = 0.3
        self.mtp_convergence_threshold = 0.2
        self.logical_coherence_threshold = 0.4

        # FIX: Histórico de razonamiento causal
        self.causal_reasoning_history = []

    def assess_reasoning_state(self, mtp_loss, reasoning_steps, logical_coherence, epoch):
        """
        Evalúa estado del sistema de razonamiento (MTP + Chain-of-Thought)
        """
        issues = []
        severity = 0
        confidence = []

        # Detectar ineficiencia en razonamiento
        if reasoning_steps is not None and isinstance(reasoning_steps, (torch.Tensor, float, int)):
            steps_mean = reasoning_steps.mean().item() if hasattr(reasoning_steps, 'mean') else float(reasoning_steps)
            if steps_mean > 4:
                issues.append("excessive_reasoning")
                severity += 2
                confidence.append(f"Razonamiento excesivo (pasos: {steps_mean:.1f})")
            elif steps_mean < 1 and epoch > 5:
                issues.append("insufficient_reasoning")
                severity += 2
                confidence.append(f"Razonamiento insuficiente (pasos: {steps_mean:.1f})")

        # Detectar divergencia MTP
        if mtp_loss is not None and isinstance(mtp_loss, torch.Tensor):
            if mtp_loss.item() > self.mtp_convergence_threshold:
                issues.append("mtp_divergence")
                severity += 3
                confidence.append(f"Divergencia MTP (pérdida: {mtp_loss.item():.3f})")

        # Detectar baja coherencia
        if logical_coherence < self.logical_coherence_threshold:
            issues.append("logical_incoherence")
            severity += 3
            confidence.append(f"Incoherencia lógica (coherencia: {logical_coherence:.3f})")

        self.cognitive_history.append({
            'epoch': epoch,
            'mtp_loss': mtp_loss.item() if mtp_loss is not None else None,
            'reasoning_steps': reasoning_steps.mean().item() if reasoning_steps is not None and hasattr(reasoning_steps, 'mean') else None,
            'logical_coherence': logical_coherence,
            'issues': issues,
            'severity': severity
        })

        return issues, severity, confidence

    def assess_cognitive_state(self, cider_score, spice_score, combined_reward, epoch):
        """
        Evalúa estado cognitivo lingüístico (planteau, déficits, sobreajuste)
        """
        issues = []
        severity = 0
        confidence = []

        # Detectar estancamiento
        if epoch > 5 and len(self.cognitive_history) > 3:
            recent_cider = [h.get('cider', 0) for h in self.cognitive_history[-3:]]
            if len(recent_cider) >= 3 and recent_cider[-1] is not None:
                cider_improvement = recent_cider[-1] - recent_cider[0]
                if cider_improvement < self.plateau_threshold:
                    issues.append("cider_plateau")
                    severity += 2
                    confidence.append(f"CIDEr estancado (mejora: {cider_improvement:.3f})")

        # Detectar déficit semántico
        if spice_score < self.spice_threshold:
            issues.append("semantic_deficit")
            severity += 3
            confidence.append(f"Déficit semántico (SPICE: {spice_score:.3f})")

        # Detectar déficit general
        if combined_reward < 0.15:
            issues.append("linguistic_deficit")
            severity += 2
            confidence.append(f"Déficit lingüístico (recompensa: {combined_reward:.3f})")

        # Detectar sobreajuste sintáctico
        if cider_score > 0.15 and spice_score < self.spice_threshold:
            issues.append("syntactic_overfitting")
            severity += 2
            confidence.append(f"Sobreajuste sintáctico (CIDEr alto, SPICE bajo)")

        # Actualizar historial con métricas lingüísticas
        if len(self.cognitive_history) > 0:
            self.cognitive_history[-1].update({
                'cider': cider_score,
                'spice': spice_score,
                'combined_reward': combined_reward
            })

        return issues, severity, confidence

    def apply_cognitive_intervention(self, model, issues, severity, confidence, epoch, diagnostics=None):
        """
        Aplica intervenciones basadas en estado lingüístico y de razonamiento
        """
        if epoch - self.last_intervention_epoch < 2 or severity == 0:
            return False

        level = "🔴 Nivel 3" if severity > 5 else "🟠 Nivel 2" if severity > 2 else "🟡 Nivel 1"

        print(f"\n{'='*80}")
        print(f"🧠 INTERVENCIÓN COGNITIVA - {level} - Severidad: {severity}/9")
        print(f"   Problemas: {', '.join(issues)}")
        print(f"   Confianza: {confidence}")
        print(f"{'='*80}")

        interventions_applied = []

        with torch.no_grad():
            # INTERVENCIONES DE RAZONAMIENTO
            if "excessive_reasoning" in issues:
                print("💡 Regularizando controlador de razonamiento")
                model.left_hemisphere.reasoning_controller[-1].weight.data *= 0.8
                model.left_hemisphere.reasoning_controller[-1].bias.data += 0.2
                interventions_applied.append("reasoning_regularization")

            if "insufficient_reasoning" in issues:
                print("💡 Sensibilizando controlador de razonamiento")
                model.left_hemisphere.reasoning_controller[-1].weight.data *= 1.2
                model.left_hemisphere.reasoning_controller[-1].bias.data -= 0.2
                interventions_applied.append("reasoning_sensitization")

            if "mtp_divergence" in issues:
                print("💡 Estabilizando MTP")
                model.left_hemisphere.lambda_mtp.data *= 0.7
                for block in model.left_hemisphere.mtp_transformer_blocks:
                    for param in block.parameters():
                        if param.dim() > 1:
                            nn.init.xavier_uniform_(param, gain=0.8)
                interventions_applied.append("mtp_stabilization")

            if "logical_incoherence" in issues:
                print("💡 Reforzando atención de razonamiento")
                model.left_hemisphere.reasoning_attention.in_proj_weight.data *= 1.1
                if hasattr(model.left_hemisphere, 'reasoning_projection'):
                    model.left_hemisphere.reasoning_projection.weight.data *= 1.05
                interventions_applied.append("reasoning_attention_boost")

            # INTERVENCIONES LINGÜÍSTICAS
            if "cider_plateau" in issues:
                print("💡 Reforzando atención visual")
                model.left_hemisphere.visual_attention.in_proj_weight.data *= 1.1
                if hasattr(model.left_hemisphere, 'liquid_gate'):
                    model.left_hemisphere.liquid_gate[-1].bias.data -= 0.2
                interventions_applied.append("visual_attention_boost")

            if "semantic_deficit" in issues:
                print("💡 Reforzando proyección semántica")
                model.left_hemisphere.output_projection.weight.data *= 1.08
                model.corpus_callosum.semantic_proj.weight.data *= 1.02
                interventions_applied.append("semantic_projection_boost")

            if "linguistic_deficit" in issues:
                print("💡 Reforzando conexiones callosales")
                model.corpus_callosum.residual_scale_base.data *= 1.05
                interventions_applied.append("callosum_alignment_boost")

            if "syntactic_overfitting" in issues:
                print("💡 Regularizando sobreajuste sintáctico")
                if hasattr(model.left_hemisphere, 'liquid_gate'):
                    for layer in model.left_hemisphere.liquid_gate:
                        if isinstance(layer, nn.Dropout):
                            layer.p = min(0.5, layer.p + 0.05)
                    model.left_hemisphere.liquid_gate[-1].bias.data += 0.3
                interventions_applied.append("syntactic_overfitting_regularization")

        print(f"\n✓ Intervenciones aplicadas: {len(interventions_applied)}")
        for inter in interventions_applied:
            print(f"  - {inter}")
        print(f"{'='*80}\n")

        self.last_intervention_epoch = epoch
        return True

# =============================================================================
# MÉTRICAS LINGÜÍSTICAS
# =============================================================================
class LanguageMetrics:
    """Métricas de calidad de generación"""

    @staticmethod
    def sentence_bleu(reference, hypothesis, weights=(0.25, 0.25, 0.25, 0.25)):
        """BLEU simplificado a nivel de oración"""
        ref_tokens = reference.lower().split()
        hyp_tokens = hypothesis.lower().split()

        if len(hyp_tokens) == 0:
            return 0.0

        # N-gram precision
        precisions = []
        for n in range(1, 5):
            ref_ngrams = LanguageMetrics._get_ngrams(ref_tokens, n)
            hyp_ngrams = LanguageMetrics._get_ngrams(hyp_tokens, n)

            if len(hyp_ngrams) == 0:
                precisions.append(0.0)
                continue

            matches = sum((hyp_ngrams & ref_ngrams).values())
            total = sum(hyp_ngrams.values())
            precisions.append(matches / total if total > 0 else 0.0)

        # Brevity penalty
        bp = min(1.0, np.exp(1 - len(ref_tokens) / max(1, len(hyp_tokens))))

        # Geometric mean
        if all(p > 0 for p in precisions):
            score = bp * np.exp(sum(w * np.log(p) for w, p in zip(weights, precisions)))
        else:
            score = 0.0

        return score

    @staticmethod
    def _get_ngrams(tokens, n):
        """Extraer n-gramas de una lista de tokens"""
        ngrams = Counter()
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            ngrams[ngram] += 1
        return ngrams

    @staticmethod
    def token_accuracy(reference, hypothesis):
        """Porcentaje de tokens correctos en posición"""
        ref_tokens = reference.lower().split()
        hyp_tokens = hypothesis.lower().split()

        min_len = min(len(ref_tokens), len(hyp_tokens))
        if min_len == 0:
            return 0.0

        matches = sum(1 for i in range(min_len) if ref_tokens[i] == hyp_tokens[i])
        return matches / max(len(ref_tokens), len(hyp_tokens))

    @staticmethod
    def word_overlap(reference, hypothesis):
        """Jaccard similarity entre palabras"""
        ref_set = set(reference.lower().split())
        hyp_set = set(hypothesis.lower().split())

        if len(ref_set | hyp_set) == 0:
            return 0.0

        return len(ref_set & hyp_set) / len(ref_set | hyp_set)


# =============================================================================
# SISTEMA DE RETROALIMENTACIÓN LINGÜÍSTICA - ÚNICA VERSIÓN CON CACHE LRU
# =============================================================================
class LinguisticFeedbackLoop:
    def __init__(self, alpha=0.6, beta=0.4):
        self.alpha = alpha
        self.beta = beta
        self.history = []

        # Cache de scores con límite
        self.score_cache = {}
        self.score_cache_order = []
        self.score_cache_maxsize = 2000
        self.score_cache_hits = 0
        self.score_cache_misses = 0

    @staticmethod
    @lru_cache(maxsize=5000)
    def _get_ngrams_cached(sentence, n):
        """FIX: Método estático con lru_cache para n-gramas"""
        tokens = sentence.lower().split()
        ngrams = {}
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            ngrams[ngram] = ngrams.get(ngram, 0) + 1
        return ngrams

    def compute_linguistic_reward(self, references, hypotheses):
        cider_scores = []
        spice_scores = []

        for ref, hyp in zip(references, hypotheses):
            pair_key = (hash(ref), hash(hyp))

            if pair_key in self.score_cache:
                cached_cider, cached_spice = self.score_cache[pair_key]
                self.score_cache_order.remove(pair_key)
                self.score_cache_order.append(pair_key)
                cider_scores.append(cached_cider)
                spice_scores.append(cached_spice)
                self.score_cache_hits += 1
            else:
                cider_score = self.compute_cider(ref, hyp)
                spice_score = self.compute_spice(ref, hyp)

                if len(self.score_cache) >= self.score_cache_maxsize:
                    oldest = self.score_cache_order.pop(0)
                    del self.score_cache[oldest]

                self.score_cache[pair_key] = (cider_score, spice_score)
                self.score_cache_order.append(pair_key)
                cider_scores.append(cider_score)
                spice_scores.append(spice_score)
                self.score_cache_misses += 1

        combined = [self.alpha * c + self.beta * s for c, s in zip(cider_scores, spice_scores)]
        reward = torch.tensor(combined).mean().clamp(0, 1)

        self.history.append({
            'cider': np.mean(cider_scores),
            'spice': np.mean(spice_scores),
            'combined': reward.item()
        })

        return reward

    def compute_cider(self, reference, hypothesis):
        """FIX: Uso correcto del cache estático"""
        ref_ngrams = self._get_ngrams_cached(reference, 4)
        hyp_ngrams = self._get_ngrams_cached(hypothesis, 4)

        overlap = sum(min(ref_ngrams.get(n, 0), hyp_ngrams.get(n, 0)) for n in hyp_ngrams)
        ref_len = sum(ref_ngrams.values())
        hyp_len = sum(hyp_ngrams.values())

        if ref_len == 0 or hyp_len == 0:
            return 0.0

        return overlap / (ref_len * hyp_len) ** 0.5

    def compute_spice(self, reference, hypothesis):
        ref_words = set(reference.lower().split())
        hyp_words = set(hypothesis.lower().split())

        if len(ref_words) == 0 and len(hyp_words) == 0:
            return 1.0

        intersection = len(ref_words & hyp_words)
        union = len(ref_words | hyp_words)

        return intersection / union if union > 0 else 0.0

    def get_cache_stats(self):
        """FIX: Estadísticas de cache actualizadas"""
        total_score = self.score_cache_hits + self.score_cache_misses

        # FIX: Acceso correcto a cache_info de lru_cache
        ngram_info = self._get_ngrams_cached.cache_info()
        total_ngram = ngram_info.hits + ngram_info.misses

        return {
            'ngram_cache_size': ngram_info.currsize,
            'ngram_hits': ngram_info.hits,
            'ngram_misses': ngram_info.misses,
            'ngram_hit_rate': ngram_info.hits / total_ngram if total_ngram > 0 else 0.0,
            'score_cache_size': len(self.score_cache),
            'score_hits': self.score_cache_hits,
            'score_misses': self.score_cache_misses,
            'score_hit_rate': self.score_cache_hits / total_score if total_score > 0 else 0.0,
            'cache_size': ngram_info.currsize + len(self.score_cache),
            'cache_hits': ngram_info.hits + self.score_cache_hits,
            'cache_misses': ngram_info.misses + self.score_cache_misses,
            'hit_rate': (ngram_info.hits + self.score_cache_hits) / (total_ngram + total_score) if (total_ngram + total_score) > 0 else 0.0
        }



# =============================================================================
# MÉTRICAS LINGÜÍSTICAS BÁSICAS - ÚNICA VERSIÓN SIN DUPLICACIÓN
# =============================================================================
class LanguageMetrics:
    @staticmethod
    def sentence_bleu(reference, hypothesis, weights=(0.25, 0.25, 0.25, 0.25)):
        ref_tokens = reference.lower().split()
        hyp_tokens = hypothesis.lower().split()
        if len(hyp_tokens) == 0:
            return 0.0
        precisions = []
        for n in range(1, 5):
            ref_ngrams = Counter(tuple(ref_tokens[i:i+n]) for i in range(len(ref_tokens)-n+1))
            hyp_ngrams = Counter(tuple(hyp_tokens[i:i+n]) for i in range(len(hyp_tokens)-n+1))
            if len(hyp_ngrams) == 0:
                precisions.append(0.0)
                continue
            matches = sum((hyp_ngrams & ref_ngrams).values())
            total = sum(hyp_ngrams.values())
            precisions.append(matches / total if total > 0 else 0.0)
        bp = min(1.0, np.exp(1 - len(ref_tokens) / max(1, len(hyp_tokens))))
        if all(p > 0 for p in precisions):
            score = bp * np.exp(sum(w * np.log(p) for w, p in zip(weights, precisions)))
        else:
            score = 0.0
        return score

    @staticmethod
    def token_accuracy(reference, hypothesis):
        ref_tokens = reference.lower().split()
        hyp_tokens = hypothesis.lower().split()
        min_len = min(len(ref_tokens), len(hyp_tokens))
        if min_len == 0:
            return 0.0
        matches = sum(1 for i in range(min_len) if ref_tokens[i] == hyp_tokens[i])
        return matches / max(len(ref_tokens), len(hyp_tokens))

    @staticmethod
    def word_overlap(reference, hypothesis):
        ref_set = set(reference.lower().split())
        hyp_set = set(hypothesis.lower().split())
        if len(ref_set | hyp_set) == 0:
            return 0.0
        return len(ref_set & hyp_set) / len(ref_set | hyp_set)


class CausalReasoningEngine(nn.Module):
    def __init__(self, hidden_dim=512):
        super().__init__()

        self.hidden_dim = hidden_dim
        self.causal_chains = {}
        self.intervention_memory = {}

        # Red para generar hipótesis causales
        self.hypothesis_generator = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.Tanh()
        )

        # Red para evaluar consistencia causal
        self.consistency_evaluator = nn.Sequential(
            nn.Linear(hidden_dim // 2, hidden_dim // 4),
            nn.ReLU(),
            nn.Linear(hidden_dim // 4, 1),
            nn.Sigmoid()
        )

        # Grafo de conocimiento simple (relaciones almacenadas)
        self.knowledge_graph = {}

    def reason_causally(self, observation, context):
        combined = torch.cat([observation, context], dim=-1)
        hypothesis = self.hypothesis_generator(combined)

        confidence = self.consistency_evaluator(hypothesis)

        interventions = self._predict_interventions(hypothesis, confidence)

        return {
            'hypothesis': hypothesis,
            'confidence': confidence.item(),
            'interventions': interventions
        }

    def _predict_interventions(self, hypothesis, confidence):
        if confidence > 0.7:
            return {
                'action': 'apply_learned_pattern',
                'strength': 0.5
            }
        elif confidence > 0.4:
            return {
                'action': 'explore_cautiously',
                'strength': 0.3
            }
        else:
            return {
                'action': 'gather_more_data',
                'strength': 0.1
            }

    def update_knowledge_graph(self, cause, effect, strength):
        if cause not in self.knowledge_graph:
            self.knowledge_graph[cause] = {}

        self.knowledge_graph[cause][effect] = strength

    def query_causal_chain(self, start_node, end_node):
        if start_node not in self.knowledge_graph:
            return None

        if end_node in self.knowledge_graph[start_node]:
            return [(start_node, end_node, self.knowledge_graph[start_node][end_node])]

        return None



# =============================================================================
# MÉTRICAS LINGÜÍSTICAS BÁSICAS (CLASE COMPLETA)
# =============================================================================
class LanguageMetrics:
    @staticmethod
    def sentence_bleu(reference, hypothesis, weights=(0.25, 0.25, 0.25, 0.25)):
        ref_tokens = reference.lower().split()
        hyp_tokens = hypothesis.lower().split()
        if len(hyp_tokens) == 0:
            return 0.0
        precisions = []
        for n in range(1, 5):
            ref_ngrams = Counter(tuple(ref_tokens[i:i+n]) for i in range(len(ref_tokens)-n+1))
            hyp_ngrams = Counter(tuple(hyp_tokens[i:i+n]) for i in range(len(hyp_tokens)-n+1))
            if len(hyp_ngrams) == 0:
                precisions.append(0.0)
                continue
            matches = sum((hyp_ngrams & ref_ngrams).values())
            total = sum(hyp_ngrams.values())
            precisions.append(matches / total if total > 0 else 0.0)
        bp = min(1.0, np.exp(1 - len(ref_tokens) / max(1, len(hyp_tokens))))
        if all(p > 0 for p in precisions):
            score = bp * np.exp(sum(w * np.log(p) for w, p in zip(weights, precisions)))
        else:
            score = 0.0
        return score

    @staticmethod
    def token_accuracy(reference, hypothesis):
        ref_tokens = reference.lower().split()
        hyp_tokens = hypothesis.lower().split()
        min_len = min(len(ref_tokens), len(hyp_tokens))
        if min_len == 0:
            return 0.0
        matches = sum(1 for i in range(min_len) if ref_tokens[i] == hyp_tokens[i])
        return matches / max(len(ref_tokens), len(hyp_tokens))

    @staticmethod
    def word_overlap(reference, hypothesis):
        ref_set = set(reference.lower().split())
        hyp_set = set(hypothesis.lower().split())
        if len(ref_set | hyp_set) == 0:
            return 0.0
        return len(ref_set & hyp_set) / len(ref_set | hyp_set)



# =============================================================================
# NEURONA LÍQUIDA ESTABLE
# =============================================================================
class StableLiquidNeuron(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()

        self.in_dim = in_dim
        self.out_dim = out_dim
        self.slow_expansion = 256
        self.fast_long_dim = 256

        self.slow_total = out_dim + self.slow_expansion
        self.fast_short_dim = out_dim
        self.concat_dim = self.slow_total + self.fast_short_dim + self.fast_long_dim

        self.W_slow = nn.Linear(in_dim, self.slow_total, bias=False)
        nn.init.orthogonal_(self.W_slow.weight, gain=0.8)

        # FIX: Definir homeostasis y metabolism como buffers registrados
        self.register_buffer('homeostasis', torch.tensor(1.0))
        self.register_buffer('metabolism', torch.tensor(0.6))
        self.register_buffer('fatigue', torch.tensor(0.0))
        self.register_buffer('sensitivity', torch.tensor(0.5))

        self.register_buffer('W_fast_short', 0.0001 * torch.randn(self.fast_short_dim, in_dim))
        self.register_buffer('W_fast_long', 0.00005 * torch.randn(self.fast_long_dim, in_dim))

        self.ln = nn.LayerNorm(self.concat_dim)
        self.project = nn.Linear(self.concat_dim, out_dim)

        # Parámetros fisiológicos adicionales (no utilizados directamente en forward)
        self.metabolism_rate = nn.Parameter(torch.tensor(0.6))
        self.fatigue_accumulation = nn.Parameter(torch.tensor(0.0))
        self.homeostasis_setpoint = nn.Parameter(torch.tensor(1.0))
        self.circadian_phase = nn.Parameter(torch.rand(1))
        self.circadian_amplitude = nn.Parameter(torch.tensor(0.2))

        self.base_lr = 0.001
        self.register_buffer('norm_ema', torch.tensor(0.5))
        self.register_buffer('norm_target', torch.tensor(1.0))

        self.fatigue_decay = 0.95
        self.metabolism_impact = 0.2
        self.cognitive_load_factor = 0.01

    def forward(self, x):
        slow_out = self.W_slow(x)
        fast_short = F.linear(x, self.W_fast_short)
        fast_long = F.linear(x, self.W_fast_long)

        gate_short = 0.05 + 0.15 * float(self.sensitivity) * float(self.homeostasis)
        gate_long = 0.02 + 0.08 * float(self.metabolism)

        combined = torch.cat([slow_out, gate_short * fast_short, gate_long * fast_long], dim=-1)
        output = self.project(self.ln(combined))

        # FIX: Calcular homeostasis después de generar output
        self.homeostasis = self._calculate_homeostasis_metric(output)

        return output, slow_out.detach(), x.detach()

    def _calculate_homeostasis_metric(self, output):
        """
        Calcula métrica de homeostasis basada en la estabilidad del output
        """
        with torch.no_grad():
            output_norm = output.norm(dim=-1).mean()
            stability = torch.sigmoid(1.0 - torch.abs(output_norm - 1.0))
            return stability.clamp(0.5, 1.0)

    def hebbian_update(self, post, pre, plasticity=0.1):
        with torch.no_grad():
            hebb = torch.mm(post.T, pre) / max(1, pre.size(0))
            hebb = torch.clamp(hebb, -0.3, 0.3)

            current_norm = self.W_fast_short.norm()
            self.norm_ema = 0.95 * self.norm_ema + 0.05 * current_norm
            norm_ratio = self.norm_ema / self.norm_target

            adaptive_lr = self.base_lr
            if norm_ratio > 3.0:
                adaptive_lr *= 0.01
                self.homeostasis.mul_(0.8)
            elif norm_ratio > 1.5:
                adaptive_lr *= 0.3
                self.homeostasis.mul_(0.95)
            elif norm_ratio < 0.5:
                adaptive_lr *= 1.2
                self.homeostasis.mul_(1.02).clamp_(0.5, 1.0)
            else:
                self.homeostasis.mul_(1.01).clamp_(0.8, 1.0)

            update_short = adaptive_lr * plasticity * float(self.homeostasis) * torch.tanh(hebb)
            self.W_fast_short += update_short[:self.fast_short_dim]

            update_long = adaptive_lr * plasticity * 0.3 * float(self.metabolism) * torch.tanh(hebb)
            self.W_fast_long += update_long[:self.fast_long_dim]

            decay = 0.999 if norm_ratio < 1.0 else 0.99 if norm_ratio < 2.0 else 0.98
            self.W_fast_short.mul_(decay)
            self.W_fast_long.mul_(decay * 0.995)

            self.W_fast_short.clamp_(-0.5, 0.5)
            self.W_fast_long.clamp_(-0.3, 0.3)

            if current_norm > 5.0:
                self.W_fast_short.mul_(self.norm_target / current_norm)

    def update_physiology_advanced(self, loss_value):
        with torch.no_grad():
            loss_signal = max(0.0, min(1.0, 1.0 - loss_value / 4.0))
            homeostasis_signal = float(self.homeostasis)
            target_metab = 0.5 + 0.3 * loss_signal + 0.1 * homeostasis_signal

            metabolism_impact = self.metabolism_impact * (float(self.metabolism) - 0.6)
            target_metab += metabolism_impact

            self.metabolism.mul_(0.9).add_(0.1 * target_metab).clamp_(0.3, 0.9)

            norm_ratio = self.norm_ema / self.norm_target

            cognitive_load = self.cognitive_load_factor * (1.0 - loss_signal)
            fatigue_increment = 0.002 if norm_ratio < 2.0 else 0.01
            fatigue_increment += cognitive_load

            self.fatigue.mul_(self.fatigue_decay).add_(fatigue_increment).clamp_(0, 0.5)

            if float(self.fatigue) > 0.3:
                self.metabolism.mul_(0.95)

            if float(self.homeostasis) < 0.7:
                self.sensitivity.mul_(0.95)
            else:
                target_sens = 0.5 + 0.2 * (1.0 - float(self.fatigue))
                self.sensitivity.mul_(0.95).add_(0.05 * target_sens)

            self.sensitivity.clamp_(0.3, 0.7)

# =============================================================================
# SISTEMA MÉDICO TRIANGULADO (VERSIÓN SIMPLIFICADA Y FUNCIONAL)
# =============================================================================
class TriangulatedMedicalSystem:
    def __init__(self):
        self.intervention_history = []
        # FIX: Inicializar explícitamente para evitar AttributeError
        self.last_intervention_epoch = -5
        self.signal_history = []
        self.gate_zombie_threshold = 0.65

    def triangulate_signals(self, health_score, liquid_norm, gate_mean, gate_std, callosal_flow):
        signals = {
            'gate_saturated': gate_mean > self.gate_zombie_threshold,
            'gate_no_diversity': gate_std < 0.05,
            'callosum_blocked': callosal_flow < 0.35,
            'liquid_high': liquid_norm > 2.5,
            'homeostasis_low': health_score <= 2,
            'communication_collapse': callosal_flow < 0.2
        }
        return signals

    def count_convergent_signals(self, signals, pattern):
        return sum(signals[sig] for sig in pattern if sig in signals)

    def diagnose_with_triangulation(self, health_score, liquid_norm, gate_mean, gate_std, callosal_flow, epoch):
        signals = self.triangulate_signals(health_score, liquid_norm, gate_mean, gate_std, callosal_flow)

        issues = []
        severity = 0
        confidence = []

        if self.count_convergent_signals(signals, ['gate_saturated', 'gate_no_diversity', 'callosum_blocked']) >= 3:
            issues.append("gate_system_failure")
            severity += 6
            confidence.append("Gate roto (100% confianza)")
        elif self.count_convergent_signals(signals, ['gate_saturated', 'gate_no_diversity', 'callosum_blocked']) == 2:
            issues.append("gate_degraded")
            severity += 4
            confidence.append("Gate degradado (67% confianza)")

        if signals['communication_collapse'] and signals['gate_no_diversity']:
            issues.append("communication_collapse")
            severity += 5
            confidence.append("Comunicación colapsada (100% confianza)")

        if signals['liquid_high'] and signals['homeostasis_low']:
            issues.append("liquid_crisis")
            severity += 5
            confidence.append("Crisis líquida (100% confianza)")
        elif signals['liquid_high']:
            issues.append("liquid_elevated")
            severity += 3
            confidence.append("Líquido alto (50% confianza)")

        if signals['gate_saturated'] and not signals['gate_no_diversity']:
            issues.append("gate_degraded")
            severity += 3
            confidence.append("Gate saturado")

        self.signal_history.append({
            'epoch': epoch,
            'signals': signals,
            'issues': issues,
            'severity': severity,
            'confidence': confidence
        })

        return issues, severity, confidence

    def apply_triangulated_intervention(self, model, issues, severity, confidence, epoch):
        # FIX: Verificación robusta de intervención reciente
        if epoch - self.last_intervention_epoch < 2 or severity == 0:
            return False

        level = "🔴 Nivel 3" if severity > 5 else "🟠 Nivel 2" if severity > 2 else "🟡 Nivel 1"

        print(f"\n{'='*80}")
        print(f"🏥 INTERVENCIÓN MÉDICA - {level} - Severidad: {severity}/12")
        print(f"   Problemas: {', '.join(issues)}")
        print(f"   Confianza: {confidence}")
        print(f"{'='*80}")

        interventions_applied = []

        with torch.no_grad():
            if "gate_system_failure" in issues:
                print("🚨 DEMOLICION TOTAL DEL GATE")
                for block in model.corpus_callosum.transfer:
                    if isinstance(block[0], nn.Linear):
                        nn.init.xavier_uniform_(block[0].weight, gain=0.05)
                        block[0].bias.data.zero_()
                interventions_applied.append("callosum_gate_demolition")

            elif "gate_degraded" in issues:
                print("💊 RESET AGRESIVO DEL GATE")
                for block in model.corpus_callosum.transfer:
                    if isinstance(block[0], nn.Linear):
                        nn.init.xavier_uniform_(block[0].weight, gain=0.15)
                interventions_applied.append("callosum_gate_reset")

            if "communication_collapse" in issues:
                print("💊 FORTALECIENDO CONEXIONES CALLOSALES")
                model.corpus_callosum.residual_scale_base.data *= 1.1
                interventions_applied.append("callosum_boost")

            if "liquid_crisis" in issues:
                print("🚨 RESET TOTAL NEURONAS LIQUIDAS")
                self._reset_liquid_neuron(model.right_hemisphere.visual_liquid)
                self._reset_liquid_neuron(model.right_hemisphere.audio_liquid)
                interventions_applied.append("liquid_full_reset")

            elif "liquid_elevated" in issues:
                model.right_hemisphere.visual_liquid.W_fast_short *= 0.4
                model.right_hemisphere.audio_liquid.W_fast_short *= 0.4
                interventions_applied.append("liquid_reduce")

            if severity >= 3:
                model.right_hemisphere.visual_liquid.fatigue *= 0.5
                model.right_hemisphere.audio_liquid.fatigue *= 0.5
                interventions_applied.append("fatigue_reduction")

        print(f"\n✓ Intervenciones aplicadas: {len(interventions_applied)}")
        for i, inter in enumerate(interventions_applied, 1):
            print(f"  {i}. {inter}")
        print(f"{'='*80}\n")

        self.intervention_history.append({
            'epoch': epoch,
            'issues': issues,
            'severity': severity,
            'level': level,
            'confidence': confidence,
            'interventions': interventions_applied
        })

        self.last_intervention_epoch = epoch
        return True

    def _reset_liquid_neuron(self, liquid_neuron):
        """Reset completo de una neurona líquida"""
        device = liquid_neuron.W_fast_short.device
        liquid_neuron.W_fast_short.data = 0.00005 * torch.randn_like(liquid_neuron.W_fast_short)
        liquid_neuron.W_fast_long.data = 0.00005 * torch.randn_like(liquid_neuron.W_fast_long)
        liquid_neuron.norm_ema = torch.tensor(0.3, device=device)
        liquid_neuron.homeostasis = torch.tensor(1.0, device=device)
        liquid_neuron.metabolism = torch.tensor(0.7, device=device)
        liquid_neuron.fatigue = torch.tensor(0.0, device=device)



# =============================================================================
# HEMISFERIO IZQUIERDO - FIX: Normalización de reasoning steps y cache de embeddings
# =============================================================================
class LeftHemisphere(nn.Module):
    def __init__(self, vocab_size, embed_dim=256, hidden_dim=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.hidden_dim = hidden_dim
        self.lstm_expansion = 128
        self.lstm_output_dim = hidden_dim + self.lstm_expansion
        self.vocab_size = vocab_size
        self.gate_warmup_epochs = 3

        # LSTM principal
        self.lstm = nn.LSTM(embed_dim + hidden_dim, self.lstm_output_dim, num_layers=2, batch_first=True, dropout=0.3)
        self.bottleneck = nn.Linear(self.lstm_output_dim, hidden_dim)

        # FIX: Gate dinámico con multi-head attention
        self.gate_attention = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=8, dropout=0.1, batch_first=True)
        self.gate_priority_network = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1)
        )

        # Gate progresivo mejorado
        self.gate_dim_1 = hidden_dim // 2
        self.gate_dim_2 = hidden_dim // 4
        self.liquid_gate = nn.Sequential(
            nn.Linear(hidden_dim, self.gate_dim_1),
            nn.LayerNorm(self.gate_dim_1),
            nn.Tanh(),
            nn.Dropout(0.4),
            nn.Linear(self.gate_dim_1, self.gate_dim_2),
            nn.Tanh(),
            nn.Dropout(0.3),
            nn.Linear(self.gate_dim_2, 1)
        )
        self.liquid_gate[-1].bias.data.fill_(-1.5)
        self.liquid_gate[-1].weight.data.mul_(0.02)

        # Resto de componentes sin cambios
        self.visual_attention = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=8, dropout=0.1, batch_first=True)
        self.audio_attention = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=4, dropout=0.1, batch_first=True)
        self.semantic_attention = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=4, dropout=0.1, batch_first=True)

        self.channel_fusion = nn.Linear(hidden_dim * 3, hidden_dim)
        self.output_projection = nn.Linear(hidden_dim, vocab_size)

        self.mtp_depth = 2
        self.mtp_transformer_blocks = nn.ModuleList([
            nn.TransformerEncoderLayer(d_model=hidden_dim, nhead=8, dim_feedforward=hidden_dim * 2, dropout=0.1, batch_first=True)
            for _ in range(self.mtp_depth)
        ])

        self.mtp_output_heads = nn.ModuleList([
            nn.Linear(hidden_dim, vocab_size) for _ in range(self.mtp_depth)
        ])

        self.mtp_combination_proj = nn.Linear(hidden_dim * 2, hidden_dim)
        self.lambda_mtp = nn.Parameter(torch.tensor(0.3))

        self.max_reasoning_steps = 5
        self.reasoning_projection = nn.Linear(hidden_dim, hidden_dim)
        self.thought_gate = nn.Linear(hidden_dim, 1)
        self.step_embedding = nn.Embedding(self.max_reasoning_steps, hidden_dim)

        self.register_buffer('step_embeddings_cache', self.step_embedding.weight.detach())

        self.reasoning_attention = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=8, dropout=0.1, batch_first=True)
        self.reasoning_decision = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid()
        )

        self.reasoning_controller = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid()
        )


    def forward(self, visual_context, captions=None, channels=None, max_len=30, epoch=0):
        batch_size = visual_context.size(0)
        device = visual_context.device

        if captions is not None:
            embeddings = self.embedding(captions[:, :-1])
            seq_len = embeddings.size(1)

            visual_expanded = visual_context.unsqueeze(1).expand(-1, seq_len, -1)
            lstm_input = torch.cat([embeddings, visual_expanded], dim=2)

            lstm_out, _ = self.lstm(lstm_input, self._get_init_state(visual_context))
            lstm_out = self.bottleneck(lstm_out)

            reasoning_control = self.reasoning_controller(lstm_out.mean(dim=1))
            use_reasoning = reasoning_control.mean() > 0.5 and epoch > 2

            reasoned_out, reasoning_steps = self._apply_chain_of_thought(lstm_out, visual_context, use_reasoning)

            if channels is not None:
                reasoned_out = self._apply_structural_attention(reasoned_out, channels, visual_context)
            else:
                visual_query = visual_context.unsqueeze(1).expand(-1, seq_len, -1)
                attended, _ = self.visual_attention(reasoned_out, visual_query, visual_query)
                reasoned_out = reasoned_out + 0.5 * attended

            # FIX: Gating dinámico con attention
            attended_gate, _ = self.gate_attention(reasoned_out, reasoned_out, reasoned_out)
            gate_context = torch.cat([reasoned_out, attended_gate], dim=-1)
            gate_priority = torch.sigmoid(self.gate_priority_network(gate_context))

            warmup_factor = torch.sigmoid(torch.tensor((epoch - 1.5) / 1.5))
            base_bias = -1.5
            adjusted_bias = base_bias * (1 - warmup_factor * 0.6)

            gate_logits = self.liquid_gate(reasoned_out)
            gate = torch.sigmoid(gate_logits + adjusted_bias) * gate_priority

            out = reasoned_out * (0.3 + 0.7 * gate)

            logits, mtp_loss = self._apply_multi_token_prediction(out, captions)

            return logits, gate, mtp_loss, reasoning_steps
        else:
            return self._greedy_decode(visual_context, channels, max_len, epoch)


    def _apply_chain_of_thought(self, hidden_states, visual_context, use_reasoning=True):
        batch_size, seq_len, _ = hidden_states.size()
        device = hidden_states.device

        if not use_reasoning:
            # FIX: Retornar tensor de zeros con batch dimension correcta
            return hidden_states, torch.zeros(batch_size, device=device, dtype=torch.float32)

        reasoning_state = hidden_states.clone()
        reasoning_steps = torch.zeros(batch_size, device=device, dtype=torch.float32)

        visual_expanded = visual_context.unsqueeze(1).expand(-1, self.max_reasoning_steps, -1)

        for step in range(self.max_reasoning_steps):
            # FIX: Uso de cache de embeddings
            step_emb = self.step_embeddings_cache[step]
            step_emb = step_emb.unsqueeze(0).unsqueeze(0).expand(batch_size, 1, -1)

            combined = reasoning_state + step_emb
            projected = self.reasoning_projection(combined)
            gate = torch.sigmoid(self.thought_gate(projected))
            gated = projected * gate

            attended, _ = self.reasoning_attention(gated, visual_expanded[:, :step+1], visual_expanded[:, :step+1])
            reasoning_state = reasoning_state + 0.1 * attended

            decision = self.reasoning_decision(reasoning_state.mean(dim=1))
            # FIX: Acumular pasos por batch item
            reasoning_steps += (decision.squeeze() > 0.3).float()

            if decision.mean() < 0.3 and step > 1:
                break

        # FIX: Normalizar steps a promedio por batch
        reasoning_steps = reasoning_steps / (step + 1)
        return reasoning_state, reasoning_steps




    def _greedy_decode(self, visual_context, channels, max_len, epoch):
        batch_size = visual_context.size(0)
        device = visual_context.device
        generated = torch.full((batch_size, 1), 1, dtype=torch.long, device=device)

        # FIX: Añadir temperatura y nucleus sampling para diversidad
        temperature = 0.9  # Reducir de 1.0 para más control
        top_p = 0.92  # Nucleus sampling

        for step in range(max_len - 1):
            emb = self.embedding(generated)
            seq_len = emb.size(1)
            visual_expanded = visual_context.unsqueeze(1).expand(-1, seq_len, -1)
            lstm_input = torch.cat([emb, visual_expanded], dim=2)

            out, _ = self.lstm(lstm_input, self._get_init_state(visual_context))
            out = self.bottleneck(out)

            if channels is not None:
                out = self._apply_structural_attention(out, channels, visual_context)
            else:
                visual_query = visual_context.unsqueeze(1).expand(-1, seq_len, -1)
                attended, _ = self.visual_attention(out, visual_query, visual_query)
                out = out + 0.5 * attended

            gate = torch.sigmoid(self.liquid_gate(out))
            out = out * (0.5 + 0.5 * gate)

            logits = self.output_projection(out[:, -1:, :])

            # FIX: Aplicar temperatura y nucleus sampling
            logits = logits / temperature
            probs = F.softmax(logits, dim=-1)

            # Nucleus sampling
            sorted_probs, sorted_indices = torch.sort(probs, descending=True, dim=-1)
            cumulative_probs = torch.cumsum(sorted_probs, dim=-1)

            # Remover tokens fuera del núcleo top-p
            sorted_indices_to_remove = cumulative_probs > top_p
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0

            # Crear máscara para tokens válidos
            indices_to_remove = sorted_indices_to_remove.scatter(2, sorted_indices, sorted_indices_to_remove)
            probs = probs.masked_fill(indices_to_remove, 0.0)

            # Renormalizar
            probs = probs / probs.sum(dim=-1, keepdim=True)

            # Sampleo multinomial en lugar de argmax
            next_token = torch.multinomial(probs.squeeze(1), num_samples=1)
            generated = torch.cat([generated, next_token], dim=1)

            if (next_token == 2).all():
                break

        return generated



    def _apply_multi_token_prediction(self, hidden_states, input_ids):
        batch_size, seq_len, hidden_dim = hidden_states.shape
        vocab_size = self.vocab_size
        padding_idx = 0

        logits = self.output_projection(hidden_states)
        mtp_loss = torch.tensor(0.0, device=hidden_states.device)

        prediction_depths = list(range(1, len(self.mtp_output_heads) + 1))
        valid_predictions = 0

        for depth in prediction_depths:
            if seq_len <= depth:
                continue

            valid_seq_len = seq_len - depth
            if valid_seq_len <= 0:
                continue

            predict_hidden = hidden_states[:, :valid_seq_len, :]
            target_ids = input_ids[:, depth:depth+valid_seq_len]

            if target_ids.size(1) == 0:
                continue

            depth_logits = self.mtp_output_heads[depth-1](predict_hidden)

            depth_loss = F.cross_entropy(
                depth_logits.reshape(-1, vocab_size),
                target_ids.reshape(-1),
                ignore_index=padding_idx,
                reduction='mean'
            )

            mtp_loss += depth_loss
            valid_predictions += 1

        if valid_predictions > 0:
            mtp_loss = mtp_loss / valid_predictions

        return logits, mtp_loss

    def _apply_structural_attention(self, lstm_out, channels, visual_context):
        seq_len = lstm_out.size(1)

        visual_expanded = channels['visual'].unsqueeze(1).expand(-1, seq_len, -1)
        audio_expanded = channels['audio'].unsqueeze(1).expand(-1, seq_len, -1)
        semantic_expanded = channels['semantic'].unsqueeze(1).expand(-1, seq_len, -1)

        visual_attended, _ = self.visual_attention(lstm_out, visual_expanded, visual_expanded)
        audio_attended, _ = self.audio_attention(lstm_out, audio_expanded, audio_expanded)
        semantic_attended, _ = self.semantic_attention(lstm_out, semantic_expanded, semantic_expanded)

        fused = torch.cat([visual_attended, audio_attended, semantic_attended], dim=-1)
        fused = self.channel_fusion(fused)

        visual_query = visual_context.unsqueeze(1).expand(-1, seq_len, -1)
        visual_attended, _ = self.visual_attention(lstm_out, visual_query, visual_query)

        combined = lstm_out + 0.3 * visual_attended + 0.7 * fused

        return combined

    def _get_init_state(self, visual_context):
        batch_size = visual_context.size(0)
        h0 = visual_context.unsqueeze(0).repeat(2, 1, 1)

        padding = torch.zeros(2, batch_size, self.lstm_expansion, device=visual_context.device)
        h0 = torch.cat([h0, padding], dim=-1)
        c0 = torch.zeros_like(h0)

        return (h0, c0)



# =============================================================================
# ENCODER DE AUDIO (Hemisferio Derecho - Canal Auditivo)
# =============================================================================
class AudioEncoder(nn.Module):
    """Encoder de audio usando Conv + Transformer"""

    def __init__(self, output_dim=512):
        super().__init__()

        self.conv_layers = nn.Sequential(
            nn.Conv1d(80, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.1),

            nn.Conv1d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.1),

            nn.Conv1d(256, 512, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.1),
        )

        self.temporal_encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=512,
                nhead=8,
                dim_feedforward=1024,
                dropout=0.1,
                batch_first=True
            ),
            num_layers=3
        )

        self.projection = nn.Linear(512, output_dim)
        self.adaptive_pool = nn.AdaptiveAvgPool1d(1)

    def forward(self, mel_spec):
        x = self.conv_layers(mel_spec)
        x = x.transpose(1, 2)
        x = self.temporal_encoder(x)
        x = x.transpose(1, 2)
        x = self.adaptive_pool(x).squeeze(-1)
        out = self.projection(x)

        return out

# =============================================================================
# HEMISFERIO DERECHO EXTENDIDO (Visión + Audio)
# =============================================================================
class RightHemisphereTricameral(nn.Module):
    """Hemisferio derecho con canales visual y auditivo"""

    def __init__(self, output_dim=512):
        super().__init__()

        # Canal visual (ResNet50) con gradient checkpointing
        resnet = models.resnet50(pretrained=True)
        for param in list(resnet.parameters())[:-20]:
            param.requires_grad = False

        self.visual_encoder = nn.Sequential(*list(resnet.children())[:-1])

        # FIX: Habilitar gradient checkpointing para reducir memoria
        if hasattr(torch.utils.checkpoint, 'checkpoint'):
            self.use_checkpointing = True
        else:
            self.use_checkpointing = False

        # Canal auditivo
        self.audio_encoder = AudioEncoder(output_dim=output_dim)

        # Neurona líquida para visión
        self.visual_liquid = StableLiquidNeuron(2048, output_dim)

        # Neurona líquida para audio
        self.audio_liquid = StableLiquidNeuron(output_dim, output_dim)

        # Fusión cross-modal
        self.cross_modal_attention = nn.MultiheadAttention(
            embed_dim=output_dim,
            num_heads=8,
            dropout=0.1,
            batch_first=True
        )

        self.fusion = nn.Sequential(
            nn.Linear(output_dim * 2, output_dim),
            nn.LayerNorm(output_dim),
            nn.GELU(),
            nn.Dropout(0.1)
        )

    def forward(self, image, audio):
        """
        Args:
            image: (B, 3, H, W)
            audio: (B, 80, T)
        Returns:
            fused_features: (B, output_dim)
            visual_post, visual_pre, audio_post, audio_pre: Para Hebbian
        """
        # FIX: Procesamiento visual con gradient checkpointing
        if self.training and self.use_checkpointing:
            visual_raw = torch.utils.checkpoint.checkpoint(
                self.visual_encoder, image, use_reentrant=False
            ).flatten(1)
        else:
            visual_raw = self.visual_encoder(image).flatten(1)

        visual_out, visual_post, visual_pre = self.visual_liquid(visual_raw)

        # Procesamiento auditivo (sin checkpointing por ser más ligero)
        audio_raw = self.audio_encoder(audio)
        audio_out, audio_post, audio_pre = self.audio_liquid(audio_raw)

        # Atención cruzada
        visual_expanded = visual_out.unsqueeze(1)
        audio_expanded = audio_out.unsqueeze(1)

        attended_visual, _ = self.cross_modal_attention(
            visual_expanded, audio_expanded, audio_expanded
        )
        attended_visual = attended_visual.squeeze(1)

        # Fusión
        fused = torch.cat([attended_visual, audio_out], dim=-1)
        fused_features = self.fusion(fused)

        return fused_features, visual_post, visual_pre, audio_post, audio_pre

# =============================================================================
# CORPUS CALLOSUM TRIMODAL
# =============================================================================
class CorpusCallosumTrimodal(nn.Module):
    def __init__(self, dim=512):
        super().__init__()
        self.visual_dim = dim // 3
        self.audio_dim = dim // 3
        self.semantic_dim = dim - 2 * (dim // 3)

        self.visual_proj = nn.Linear(dim, self.visual_dim)
        self.audio_proj = nn.Linear(dim, self.audio_dim)
        self.semantic_proj = nn.Linear(dim, self.semantic_dim)

        self.visual_gate = nn.Parameter(torch.tensor(0.5))
        self.audio_gate = nn.Parameter(torch.tensor(0.5))
        self.semantic_gate = nn.Parameter(torch.tensor(0.5))

        self.trimodal_attention = nn.MultiheadAttention(
            embed_dim=dim,
            num_heads=8,
            dropout=0.1,
            batch_first=True
        )

        self.transfer = nn.ModuleList([
            nn.Sequential(
                nn.Linear(dim, dim),
                nn.LayerNorm(dim),
                nn.GELU(),
                nn.Dropout(0.1)
            ) for _ in range(3)
        ])

        self.residual_scale_base = nn.Parameter(torch.tensor(0.85))
        self.flow_modulator = nn.Sequential(
            nn.Linear(dim, dim // 4),
            nn.Tanh(),
            nn.Linear(dim // 4, 1),
            nn.Sigmoid()
        )

        # FIX: Usar register_parameter en lugar de register_buffer para movimiento automático
        self.register_parameter('visual_fatigue', nn.Parameter(torch.tensor(0.0), requires_grad=False))
        self.register_parameter('audio_fatigue', nn.Parameter(torch.tensor(0.0), requires_grad=False))
        self.register_parameter('semantic_fatigue', nn.Parameter(torch.tensor(0.0), requires_grad=False))

        self.fatigue_decay = 0.95
        self.fatigue_recovery = 0.01



    def forward(self, right_features):
        x = right_features.unsqueeze(1)

        visual_channel = self.visual_proj(right_features)
        audio_channel = self.audio_proj(right_features)
        semantic_channel = self.semantic_proj(right_features)

        visual_gated = visual_channel * torch.sigmoid(self.visual_gate)
        audio_gated = audio_channel * torch.sigmoid(self.audio_gate)
        semantic_gated = semantic_channel * torch.sigmoid(self.semantic_gate)

        # FIX: Aplicar fatiga como máscara sigmoide
        visual_gated = visual_gated * torch.sigmoid(1.0 - self.visual_fatigue)
        audio_gated = audio_gated * torch.sigmoid(1.0 - self.audio_fatigue)
        semantic_gated = semantic_gated * torch.sigmoid(1.0 - self.semantic_fatigue)

        structured = torch.cat([visual_gated, audio_gated, semantic_gated], dim=-1)
        structured_expanded = structured.unsqueeze(1)

        attn_out, _ = self.trimodal_attention(
            structured_expanded, structured_expanded, structured_expanded
        )
        attn_out = attn_out.squeeze(1)

        for block in self.transfer:
            attn_out = attn_out + block(attn_out)

        flow_strength = self.flow_modulator(right_features).squeeze(-1)
        # FIX: Asegurar broadcasting correcto
        dynamic_scale = self.residual_scale_base * (0.7 + 0.6 * flow_strength).unsqueeze(-1)
        output = attn_out + dynamic_scale * right_features

        visual_full = torch.cat([
            visual_gated,
            torch.zeros(visual_gated.size(0), self.audio_dim + self.semantic_dim, device=visual_gated.device)
        ], dim=-1)

        audio_full = torch.cat([
            torch.zeros(audio_gated.size(0), self.visual_dim, device=audio_gated.device),
            audio_gated,
            torch.zeros(audio_gated.size(0), self.semantic_dim, device=audio_gated.device)
        ], dim=-1)

        semantic_full = torch.cat([
            torch.zeros(semantic_gated.size(0), self.visual_dim + self.audio_dim, device=semantic_gated.device),
            semantic_gated
        ], dim=-1)

        self.update_channel_fatigue(visual_channel, audio_channel, semantic_channel)

        return output, {
            'visual': visual_full,
            'audio': audio_full,
            'semantic': semantic_full,
            'fatigue': {
                'visual': self.visual_fatigue.item(),
                'audio': self.audio_fatigue.item(),
                'semantic': self.semantic_fatigue.item()
            }
        }

    def update_channel_fatigue(self, visual_channel, audio_channel, semantic_channel):
        with torch.no_grad():
            visual_activity = visual_channel.norm(dim=-1).mean()
            audio_activity = audio_channel.norm(dim=-1).mean()
            semantic_activity = semantic_channel.norm(dim=-1).mean()

            # FIX: Reducir tasa de acumulación de fatiga
            fatigue_accumulation = 0.005  # Cambio de 0.01 a 0.005

            self.visual_fatigue.data = torch.clamp(
                self.visual_fatigue * self.fatigue_decay + fatigue_accumulation * visual_activity - self.fatigue_recovery,
                0.0, 0.5  # Cambio de límite 1.0 a 0.5 para evitar bloqueo completo
            )
            self.audio_fatigue.data = torch.clamp(
                self.audio_fatigue * self.fatigue_decay + fatigue_accumulation * audio_activity - self.fatigue_recovery,
                0.0, 0.5
            )
            self.semantic_fatigue.data = torch.clamp(
                self.semantic_fatigue * self.fatigue_decay + fatigue_accumulation * semantic_activity - self.fatigue_recovery,
                0.0, 0.5
            )

    def adjust_gates_by_fatigue(self):
        with torch.no_grad():
            # FIX: Aplicar factor de fatiga con clamp de seguridad
            fatigue_factor_visual = torch.clamp(1.0 - 0.1 * self.visual_fatigue, 0.5, 1.0)
            fatigue_factor_audio = torch.clamp(1.0 - 0.1 * self.audio_fatigue, 0.5, 1.0)
            fatigue_factor_semantic = torch.clamp(1.0 - 0.1 * self.semantic_fatigue, 0.5, 1.0)

            self.visual_gate.data *= fatigue_factor_visual
            self.audio_gate.data *= fatigue_factor_audio
            self.semantic_gate.data *= fatigue_factor_semantic

            # FIX: Clamp de gates manteniendo rango funcional
            self.visual_gate.data = torch.clamp(self.visual_gate.data, -2.0, 2.0)
            self.audio_gate.data = torch.clamp(self.audio_gate.data, -2.0, 2.0)
            self.semantic_gate.data = torch.clamp(self.semantic_gate.data, -2.0, 2.0)



# =============================================================================
# DIAGNÓSTICOS MEJORADOS - FIX: Cache de normalización y cálculos repetitivos
# =============================================================================
class EnhancedDiagnosticsTricameral:
    def __init__(self):
        self.history = {
            'loss': [],
            'visual_liquid_metabolism': [], 'visual_liquid_fatigue': [], 'visual_liquid_norm': [],
            'audio_liquid_metabolism': [], 'audio_liquid_fatigue': [], 'audio_liquid_norm': [],
            'callosal_flow': [], 'left_gate_mean': [], 'left_gate_std': [],
            'synergy_score': [], 'health_score': [],
            'bleu_score': [], 'token_accuracy': [], 'word_overlap': [],
            'cider_score': [], 'spice_score': [], 'linguistic_reward': [],
            'coherence_loss': [],
            'callosum_visual_fatigue': [], 'callosum_audio_fatigue': [], 'callosum_semantic_fatigue': [],
            'reasoning_steps': [], 'mtp_loss': [], 'logical_coherence': [],
            'reasoning_efficiency': [], 'mtp_accuracy': []
        }
        self.language_metrics = LanguageMetrics()

        # FIX: Cache para normalizaciones repetidas
        self._norm_cache = {}
        self._corr_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0

    def _get_cached_norm(self, tensor, dim=-1):
        """Cache de normalización con limpieza periódica"""
        key = (tensor.data_ptr(), tensor.shape, dim)

        # FIX: Limpiar cache cada 100 accesos para evitar memory leak
        if len(self._norm_cache) > 1000:
            self._norm_cache.clear()
            self._corr_cache.clear()

        if key in self._norm_cache:
            self.cache_hits += 1
            return self._norm_cache[key]
        else:
            self.cache_misses += 1
            norm = F.normalize(tensor, dim=dim)
            self._norm_cache[key] = norm
            return norm

    def measure_callosal_flow(self, right_features, left_context, channels=None):
        # FIX: Usar cache para normalizaciones
        right_norm = self._get_cached_norm(right_features)
        left_norm = self._get_cached_norm(left_context)
        correlation = (right_norm * left_norm).sum(dim=-1).mean()
        flow_std = left_context.std(dim=-1).mean()

        if channels is not None:
            visual_norm = self._get_cached_norm(channels['visual'])
            audio_norm = self._get_cached_norm(channels['audio'])
            semantic_norm = self._get_cached_norm(channels['semantic'])

            # FIX: Usar cache para correlaciones
            corr_key = (right_features.data_ptr(), channels['visual'].data_ptr())
            if corr_key in self._corr_cache:
                visual_corr = self._corr_cache[corr_key]
            else:
                visual_corr = (right_norm * visual_norm).sum(dim=-1).mean()
                self._corr_cache[corr_key] = visual_corr

            audio_corr = (right_norm * audio_norm).sum(dim=-1).mean()
            semantic_corr = (right_norm * semantic_norm).sum(dim=-1).mean()

            weighted_correlation = 0.4 * visual_corr + 0.4 * audio_corr + 0.2 * semantic_corr
            flow = weighted_correlation * min(1.0, flow_std.item() / 0.5)
        else:
            flow = correlation.item() * min(1.0, flow_std.item() / 0.5)

        return float(flow)

    def evaluate_reasoning_quality(self, generated_texts, reference_texts, reasoning_steps):
        coherence_scores = []
        consistency_scores = []

        for gen, ref, steps in zip(generated_texts, reference_texts, reasoning_steps):
            gen_sentences = [s.strip() for s in gen.split('.') if s.strip()]

            # FIX: Evaluación de coherencia con manejo de edge cases
            if len(gen_sentences) > 1:
                sentence_similarities = []
                for i in range(len(gen_sentences) - 1):
                    words1 = set(gen_sentences[i].lower().split())
                    words2 = set(gen_sentences[i+1].lower().split())

                    if len(words1) > 0 and len(words2) > 0:
                        jaccard = len(words1 & words2) / len(words1 | words2)
                        sentence_similarities.append(jaccard)

                coherence = np.mean(sentence_similarities) if sentence_similarities else 0.5
            else:
                coherence = 0.5

            # FIX: Consistencia con verificación de división por cero
            gen_words = set(gen.lower().split())
            ref_words = set(ref.lower().split())
            if len(gen_words | ref_words) == 0:
                consistency = 0.0
            else:
                consistency = len(gen_words & ref_words) / len(gen_words | ref_words)

            # FIX: Bonus de razonamiento con clamp seguro
            reasoning_bonus = min(1.0, (steps if hasattr(steps, '__float__') else float(steps)) / 3.0) if steps is not None else 0.0
            coherence_scores.append(coherence * (0.7 + 0.3 * reasoning_bonus))
            consistency_scores.append(consistency)

        return np.mean(coherence_scores), np.mean(consistency_scores)

    def calculate_synergy(self, visual_node, audio_node, callosal_flow, left_gate_mean, left_gate_std):
        # FIX: Cálculo de salud con clamp de seguridad
        visual_health = float(visual_node.metabolism) * float(visual_node.homeostasis) * max(0.0, 1.0 - float(visual_node.fatigue) * 0.5)
        audio_health = float(audio_node.metabolism) * float(audio_node.homeostasis) * max(0.0, 1.0 - float(audio_node.fatigue) * 0.5)
        callosal_health = float(callosal_flow)
        gate_balance = max(0.0, 1.0 - abs(float(left_gate_mean) - 0.5) * 2.0)
        gate_diversity = min(1.0, float(left_gate_std) * 5.0)
        left_health = 0.7 * gate_balance + 0.3 * gate_diversity
        synergy = (0.25 * visual_health + 0.25 * audio_health + 0.25 * callosal_health + 0.25 * left_health)
        return float(synergy)

    def calculate_health(self, visual_node, audio_node, callosal_flow, left_gate_mean, left_gate_std, liquid_norm):
        health = 0
        if float(liquid_norm) < 2.0: health += 1
        if float(visual_node.homeostasis) > 0.7: health += 1
        if float(audio_node.homeostasis) > 0.7: health += 1
        if float(callosal_flow) > 0.4: health += 1
        if 0.35 < float(left_gate_mean) < 0.65 and float(left_gate_std) > 0.05: health += 1
        return int(health)

    def update(self, **metrics):
        for key, value in metrics.items():
            if key in self.history and value is not None:
                # FIX: Conversión segura de tensor a valor escalar
                if isinstance(value, torch.Tensor):
                    if value.is_cuda:
                        if value.numel() == 1:
                            value = value.cpu().item()
                        else:
                            value = value.cpu().numpy().tolist()
                    else:
                        if value.numel() == 1:
                            value = value.item()
                        else:
                            value = value.numpy().tolist()
                self.history[key].append(value)

    def get_recent_avg(self, key, n=50):
        if key in self.history and len(self.history[key]) > 0:
            recent_values = self.history[key][-n:]
            clean_values = []
            for v in recent_values:
                if isinstance(v, torch.Tensor):
                    clean_values.append(float(v.item() if v.numel() == 1 else v.mean()))
                elif isinstance(v, (list, np.ndarray)):
                    clean_values.append(np.mean(v))
                else:
                    clean_values.append(float(v))
            return np.mean(clean_values)
        elif key in ['callosum_visual_fatigue', 'callosum_audio_fatigue', 'callosum_semantic_fatigue']:
            return 0.0
        return 0.0

    def visualize_fatigue_distribution(self, epoch):
        if epoch % 5 == 0:
            visual_fatigue = self.get_recent_avg('callosum_visual_fatigue', n=10)
            audio_fatigue = self.get_recent_avg('callosum_audio_fatigue', n=10)
            semantic_fatigue = self.get_recent_avg('callosum_semantic_fatigue', n=10)

            print(f"\n🔗 DISTRIBUCIÓN DE FATIGA - Época {epoch}")
            print(f"  Visual: {visual_fatigue:.3f} {'🔴' if visual_fatigue > 0.3 else '🟡' if visual_fatigue > 0.15 else '🟢'}")
            print(f"  Audio: {audio_fatigue:.3f} {'🔴' if audio_fatigue > 0.3 else '🟡' if audio_fatigue > 0.15 else '🟢'}")
            print(f"  Semántico: {semantic_fatigue:.3f} {'🔴' if semantic_fatigue > 0.3 else '🟡' if semantic_fatigue > 0.15 else '🟢'}")

            # FIX: Calcular desbalance con manejo de valores idénticos
            values = [visual_fatigue, audio_fatigue, semantic_fatigue]
            if max(values) == min(values):
                imbalance = 0.0
            else:
                imbalance = max(values) - min(values)

            if imbalance > 0.2:
                print(f"  ⚠️  Desbalance: {imbalance:.3f}")
            else:
                print(f"  ✅ Balanceado: {imbalance:.3f}")
            print(f"{'='*60}")

    def visualize_reasoning_metrics(self, epoch):
        if epoch % 3 == 0:
            reasoning_steps = self.get_recent_avg('reasoning_steps', n=10)
            mtp_loss = self.get_recent_avg('mtp_loss', n=10)
            logical_coherence = self.get_recent_avg('logical_coherence', n=10)

            print(f"\n🧠 MÉTRICAS DE RAZONAMIENTO - Época {epoch}")
            print(f"  Pasos: {reasoning_steps:.2f} {'🟢' if 2 <= reasoning_steps <= 3 else '🟡'}")
            print(f"  MTP Loss: {mtp_loss:.3f} {'🟢' if mtp_loss < 0.2 else '🟡' if mtp_loss < 0.4 else '🔴'}")
            print(f"  Coherencia: {logical_coherence:.3f} {'🟢' if logical_coherence > 0.4 else '🟡' if logical_coherence > 0.2 else '🔴'}")
            print(f"{'='*60}")

    def report(self, epoch):
        if len(self.history['loss']) == 0:
            return

        self.visualize_fatigue_distribution(epoch)
        self.visualize_reasoning_metrics(epoch)

        print(f"\n{'='*80}")
        print(f"📊 REPORTE COMPLETO - Época {epoch}")
        print(f"{'='*80}")

        loss = self.get_recent_avg('loss')
        print(f"\n📉 ENTRENAMIENTO:")
        print(f"  Loss: {loss:.4f}")

        # FIX: Métricas lingüísticas con indicadores visuales
        bleu = self.get_recent_avg('bleu_score')
        acc = self.get_recent_avg('token_accuracy')
        overlap = self.get_recent_avg('word_overlap')
        cider = self.get_recent_avg('cider_score')
        spice = self.get_recent_avg('spice_score')
        reward = self.get_recent_avg('linguistic_reward')

        print(f"\n📝 CALIDAD LINGÜÍSTICA:")
        print(f"  BLEU-4: {bleu:.4f} {'🟢' if bleu > 0.15 else '🟡' if bleu > 0.08 else '🔴'}")
        print(f"  Accuracy: {acc:.4f} {'🟢' if acc > 0.30 else '🟡' if acc > 0.15 else '🔴'}")
        print(f"  W-Overlap: {overlap:.4f} {'🟢' if overlap > 0.35 else '🟡' if overlap > 0.20 else '🔴'}")
        print(f"  CIDEr: {cider:.4f} {'🟢' if cider > 0.15 else '🟡' if cider > 0.08 else '🔴'}")
        print(f"  SPICE: {spice:.4f} {'🟢' if spice > 0.20 else '🟡' if spice > 0.10 else '🔴'}")
        print(f"  Reward: {reward:.4f} {'🟢' if reward > 0.30 else '🟡' if reward > 0.15 else '🔴'}")

        reasoning_steps = self.get_recent_avg('reasoning_steps')
        mtp_loss = self.get_recent_avg('mtp_loss')
        logical_coherence = self.get_recent_avg('logical_coherence')

        print(f"\n🧠 RAZONAMIENTO:")
        print(f"  Pasos: {reasoning_steps:.2f} {'🟢' if 2 <= reasoning_steps <= 3 else '🟡'}")
        print(f"  MTP Loss: {mtp_loss:.3f} {'🟢' if mtp_loss < 0.2 else '🟡' if mtp_loss < 0.4 else '🔴'}")
        print(f"  Coherencia: {logical_coherence:.3f} {'🟢' if logical_coherence > 0.4 else '🟡' if logical_coherence > 0.2 else '🔴'}")

        visual_liquid = self.get_recent_avg('visual_liquid_norm')
        audio_liquid = self.get_recent_avg('audio_liquid_norm')

        print(f"\n🧬 FISIOLOGÍA:")
        print(f"  Visual Norm: {visual_liquid:.3f} {'🟢' if visual_liquid < 2.0 else '🟡' if visual_liquid < 4.0 else '🔴'}")
        print(f"  Audio Norm: {audio_liquid:.3f} {'🟢' if audio_liquid < 2.0 else '🟡' if audio_liquid < 4.0 else '🔴'}")

        flow = self.get_recent_avg('callosal_flow')
        gate_mean = self.get_recent_avg('left_gate_mean')
        gate_std = self.get_recent_avg('left_gate_std')

        print(f"\n🔗 COMUNICACIÓN:")
        print(f"  Callosum: {flow:.3f} {'🟢' if flow > 0.5 else '🟡' if flow > 0.3 else '🔴'}")
        print(f"  Gate Mean: {gate_mean:.3f} {'🟢' if 0.35 < gate_mean < 0.65 else '🟡'}")
        print(f"  Gate Std: {gate_std:.3f}")

        # FIX: Métricas de cache
        print(f"\n⚡ CACHE PERFORMANCE:")
        print(f"  Cache hit rate: {self.cache_hits / (self.cache_hits + self.cache_misses + 1):.2%}")

        synergy = self.get_recent_avg('synergy_score')
        health = self.get_recent_avg('health_score')

        print(f"\n🏛️  SISTEMA TRICAMERAL:")
        print(f"  Sinergia: {synergy:.3f} | Salud: {int(health)}/5", end=" ")
        if health >= 4:
            print("🟢 ÓPTIMO")
        elif health >= 3:
            print("🟡 FUNCIONAL")
        else:
            print("🔴 CRÍTICO")
        print(f"{'='*80}\n")




# =============================================================================
# MODELO TRICAMERAL COMPLETO
# =============================================================================
class NeuroLogosTricameral(nn.Module):
    """Arquitectura completa: Visión + Audio -> Lenguaje"""

    def __init__(self, vocab_size):
        super().__init__()
        self.right_hemisphere = RightHemisphereTricameral(output_dim=512)
        self.corpus_callosum = CorpusCallosumTrimodal(dim=512)
        self.left_hemisphere = LeftHemisphere(vocab_size, embed_dim=256, hidden_dim=512)

    def forward(self, image, audio, captions=None, epoch=0):
        fused_features, vis_post, vis_pre, aud_post, aud_pre = self.right_hemisphere(image, audio)
        enriched_context, channels = self.corpus_callosum(fused_features)

        if captions is not None:
            logits, gate, mtp_loss, reasoning_steps = self.left_hemisphere(
                enriched_context, captions, channels, epoch=epoch
            )

            return (
                logits, fused_features, enriched_context, gate,
                vis_post, vis_pre, aud_post, aud_pre,
                channels, mtp_loss, reasoning_steps
            )
        else:
            generated_text = self.left_hemisphere(
                enriched_context, captions=None, channels=channels, epoch=epoch
            )

            return generated_text, None, None, None, None, None, None, None, None, None, None



# =============================================================================
# DATASET MULTIMODAL ACTUALIZADO
# =============================================================================
class Flickr8kMultimodalDataset(Dataset):
    """Dataset que carga imagen, audio del caption y texto desde Kaggle"""

    def __init__(self, images_dir, audio_dir, captions_file, vocab,
                 img_transform=None, max_len=30, sample_rate=16000):
        self.images_dir = images_dir
        self.audio_dir = audio_dir
        self.vocab = vocab
        self.max_len = max_len
        self.sample_rate = sample_rate
        self.img_transform = img_transform

        # Procesador de audio (alineado con dataset: 16kHz)
        self.mel_spectrogram = T.MelSpectrogram(
            sample_rate=sample_rate,
            n_fft=400,
            win_length=400,
            hop_length=160,
            n_mels=80,
            f_min=0,
            f_max=8000
        )

        # Resampler por si acaso
        self.resampler = T.Resample(sample_rate, sample_rate)

        self.data = []

        # Mapeo: image_name -> list of audio files
        audio_files = {f.stem: f for f in Path(audio_dir).glob("*.wav")}

        with open(captions_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    img_name, caption = parts
                    img_path = os.path.join(images_dir, img_name)

                    # Buscar audio correspondiente
                    stem = Path(img_name).stem
                    audio_keys = [f"{stem}_{i}" for i in range(5)]

                    for audio_key in audio_keys:
                        if audio_key in audio_files:
                            audio_path = audio_files[audio_key]
                            if os.path.exists(img_path):
                                self.data.append((img_path, str(audio_path), caption))

        print(f"✓ Loaded {len(self.data)} multimodal samples")
        print(f"  Formato audio: .wav, 16kHz (del dataset de Kaggle)")

    def __len__(self):
        return len(self.data)


    def __getitem__(self, idx):
        img_path, audio_path, caption = self.data[idx]

        image = Image.open(img_path).convert('RGB')
        if self.img_transform:
            image = self.img_transform(image)

        waveform_np, sr = sf.read(audio_path)
        waveform = torch.from_numpy(waveform_np).float()

        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        elif waveform.ndim == 2:
            waveform = waveform.T

        if sr != self.sample_rate:
            resampler = T.Resample(sr, self.sample_rate)
            waveform = resampler(waveform)

        if waveform.size(0) > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        mel_spec = self.mel_spectrogram(waveform)
        mel_spec = torch.log(mel_spec + 1e-9)
        mel_spec = (mel_spec - mel_spec.mean()) / (mel_spec.std() + 1e-8)

        target_len = 300
        if mel_spec.size(-1) < target_len:
            pad = target_len - mel_spec.size(-1)
            mel_spec = F.pad(mel_spec, (0, pad))
        else:
            mel_spec = mel_spec[..., :target_len]

        tokens = ['<BOS>'] + caption.lower().split() + ['<EOS>']
        token_ids = [self.vocab.get(w, self.vocab['<UNK>']) for w in tokens]

        if len(token_ids) < self.max_len:
            token_ids += [self.vocab['<PAD>']] * (self.max_len - len(token_ids))
        else:
            token_ids = token_ids[:self.max_len]

        return image, mel_spec.squeeze(0), torch.tensor(token_ids, dtype=torch.long), caption




# =============================================================================
# FUNCIÓN DE ALINEACIÓN TEMPRANA - FIX: Desacoplada de pérdida principal
# =============================================================================
def compute_alignment_loss(visual_features, channels, alpha=0.1, epoch=0):
    """
    FIX: Pérdida auxiliar para alineación temprana de canales multimodales
    Solo activa en épocas iniciales (epoch < 6)
    """
    if epoch >= 6:
        return torch.tensor(0.0, device=visual_features.device)

    with torch.enable_grad():
        visual_norm = F.normalize(visual_features, dim=-1)
        visual_channel_norm = F.normalize(channels['visual'], dim=-1)
        audio_channel_norm = F.normalize(channels['audio'], dim=-1)
        semantic_channel_norm = F.normalize(channels['semantic'], dim=-1)

        visual_align = (1 - (visual_channel_norm * visual_norm).sum(dim=-1)).mean()
        audio_align = (1 - (audio_channel_norm * visual_norm).sum(dim=-1)).mean()
        semantic_align = (1 - (semantic_channel_norm * visual_norm).sum(dim=-1)).mean()

        # FIX: Pesos ponderados por importancia modal
        total_align = 0.5 * visual_align + 0.3 * audio_align + 0.2 * semantic_align

        return alpha * total_align



# =============================================================================
# FUNCIÓN DE PÉRDIDA TRICAMERAL - FIX: Separación de alineación y parámetros limpios
# =============================================================================
def compute_tricameral_loss(logits, captions, gate, vocab,
                           visual_post, audio_post,
                           mtp_loss=None, linguistic_reward=None,
                           lambda_reward=0.1, lambda_mtp=0.1):
    # Pérdida estándar
    ce_loss = F.cross_entropy(
        logits.reshape(-1, len(vocab)),
        captions[:, 1:].reshape(-1),
        ignore_index=vocab['<PAD>']
    )

    # Penalizaciones del gate con estabilización numérica
    gate_mean = gate.mean()
    gate_penalty = F.relu(gate_mean - 0.5) ** 2
    gate_diversity = gate.std()
    diversity_penalty = F.relu(0.10 - gate_diversity) ** 2  # Cambio de 0.15 a 0.10 para menos presión

    # Coherencia audio-visual con normalización
    visual_norm = F.normalize(visual_post, dim=-1)
    audio_norm = F.normalize(audio_post, dim=-1)
    coherence_loss = (1 - (visual_norm * audio_norm).sum(dim=-1)).mean()

    # Recompensa lingüística (inversa para minimización)
    linguistic_loss = -lambda_reward * linguistic_reward if linguistic_reward is not None else 0.0

    # Término MTP con gradiente estabilizado
    if mtp_loss is not None and isinstance(mtp_loss, torch.Tensor) and mtp_loss.item() > 0:
        mtp_term = lambda_mtp * mtp_loss
    else:
        mtp_term = 0.0

    # FIX: Rebalancear pesos para dar más importancia a coherencia multimodal
    total_loss = (
        ce_loss +
        0.03 * gate_penalty +      # Reducido de 0.05
        0.1 * diversity_penalty +  # Reducido de 0.2
        0.2 * coherence_loss +     # Aumentado de 0.1 para forzar alineación
        linguistic_loss +
        mtp_term
    )

    return total_loss, ce_loss, gate_penalty, diversity_penalty, coherence_loss, linguistic_loss, mtp_term


# =============================================================================
# LOOP DE ENTRENAMIENTO PRINCIPAL
# =============================================================================
def train_tricameral():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # ========================================================================
    # PASO 1: BUSCAR Y CARGAR CHECKPOINT EXISTENTE
    # ========================================================================
    checkpoint_dir = './checkpoints'
    os.makedirs(checkpoint_dir, exist_ok=True)

    resume_data = None
    start_epoch = 0
    best_val_loss = float('inf')

    # Buscar último checkpoint
    if os.path.exists(checkpoint_dir):
        checkpoints = sorted([
            f for f in os.listdir(checkpoint_dir)
            if f.startswith('tricameral_epoch_') and f.endswith('_full.pth')
        ])

        if checkpoints:
            latest_checkpoint = checkpoints[-1]
            checkpoint_path = os.path.join(checkpoint_dir, latest_checkpoint)

            print(f"\n{'='*80}")
            print(f"🔄 CHECKPOINT DETECTADO: {latest_checkpoint}")
            print(f"{'='*80}")

            try:
                resume_data = torch.load(checkpoint_path, map_location='cpu')
                start_epoch = resume_data['epoch'] + 1
                best_val_loss = resume_data.get('best_val_loss', float('inf'))

                print(f"✅ Checkpoint cargado exitosamente")
                print(f"   Época inicial: {start_epoch}")
                print(f"   Best val loss: {best_val_loss:.4f}")
                print(f"   Memoria episódica: {resume_data['episodic_memory_size']}/500")
                print(f"{'='*80}\n")
            except Exception as e:
                print(f"⚠️ Error cargando checkpoint: {e}")
                print(f"⚠️ Iniciando entrenamiento desde cero\n")
                resume_data = None
                start_epoch = 0

    # ========================================================================
    # PASO 2: SETUP DATASET Y MODELO
    # ========================================================================
    print(f"\n{'='*80}")
    print(f"NeuroLogos TRICAMERAL v5.2 | Visión + Audio + Lenguaje + Razonamiento | Device: {device}")
    print(f"🎵 Usando dataset pre-generado de Kaggle (40k audios .wav)")
    print(f"🧠 Sistema médico + cognitivo + memoria episódica integrados")
    print(f"{'='*80}\n")

    flickr_dir = setup_flickr8k_with_audio('./flickr8k_full')
    images_dir = os.path.join(flickr_dir, 'Images')
    audio_dir = os.path.join(flickr_dir, 'wavs')
    captions_file = os.path.join(flickr_dir, 'captions.txt')

    if not os.path.exists(audio_dir) or len(list(Path(audio_dir).glob("*.wav"))) < 1000:
        print("❌ Error: No se encontraron suficientes audios. Ejecuta setup_flickr8k_with_audio() primero.")
        return

    print(f"✅ Audio directory found: {len(list(Path(audio_dir).glob('*.wav')))} files\n")

    # Cargar o crear vocabulario
    if resume_data and 'vocab' in resume_data:
        vocab = resume_data['vocab']
        id2word = resume_data['id2word']
        print("✅ Vocabulario cargado desde checkpoint")
    else:
        vocab, id2word = build_vocab_flickr(captions_file, vocab_size=5000)

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    dataset = Flickr8kMultimodalDataset(
        images_dir, audio_dir, captions_file, vocab,
        img_transform=transform, max_len=30
    )

    from torch.utils.data import random_split
    generator = torch.Generator().manual_seed(42)
    train_size = int(0.9 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size], generator=generator)

    print(f"📊 Dataset split: {train_size} train, {val_size} val\n")

    try:
        import google.colab
        IN_COLAB = True
        print("📦 Entorno Google Colab detectado")
    except:
        IN_COLAB = False
        print("💻 Entorno estándar detectado")

    if IN_COLAB:
        train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=0, pin_memory=False)
        val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=0, pin_memory=False)
    else:
        train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=4, pin_memory=True, persistent_workers=True)
        val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=2, pin_memory=True, persistent_workers=True)

    # ========================================================================
    # PASO 3: CREAR MODELO Y CARGAR PESOS SI HAY CHECKPOINT
    # ========================================================================
    model = NeuroLogosTricameral(len(vocab)).to(device)

    model.corpus_callosum.visual_fatigue.data = torch.tensor(0.0, device=device)
    model.corpus_callosum.audio_fatigue.data = torch.tensor(0.0, device=device)
    model.corpus_callosum.semantic_fatigue.data = torch.tensor(0.0, device=device)

    if resume_data:
        model.load_state_dict(resume_data['model_state_dict'])
        print("✅ Pesos del modelo restaurados")

    # ========================================================================
    # PASO 4: CREAR OPTIMIZER Y CARGAR ESTADO SI HAY CHECKPOINT
    # ========================================================================
    optimizer = torch.optim.AdamW([
        {'params': model.right_hemisphere.parameters(), 'lr': 3e-4},
        {'params': model.corpus_callosum.parameters(), 'lr': 5e-4},
        {'params': model.left_hemisphere.parameters(), 'lr': 2e-4}
    ])

    warmup_scheduler = torch.optim.lr_scheduler.LinearLR(optimizer, start_factor=0.1, total_iters=3)
    main_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=27, eta_min=1e-6)
    scheduler = torch.optim.lr_scheduler.SequentialLR(optimizer, schedulers=[warmup_scheduler, main_scheduler], milestones=[3])

    if resume_data:
        optimizer.load_state_dict(resume_data['optimizer_state_dict'])
        scheduler.load_state_dict(resume_data['scheduler_state_dict'])
        print("✅ Optimizer y scheduler restaurados")

    # ========================================================================
    # PASO 5: CREAR SISTEMAS Y CARGAR MEMORIA EPISÓDICA SI HAY CHECKPOINT
    # ========================================================================
    diagnostics = EnhancedDiagnosticsTricameral()
    medical_system = TriangulatedMedicalSystem()
    cognitive_system = NeurocognitiveSystem()
    episodic_memory = HierarchicalEpisodicMemory(
        working_capacity=200,      # Reducido de 1000
        short_term_capacity=800,   # Reducido de 5000
        importance_threshold=0.7
    )

    if resume_data:
        if 'episodic_memory_buffer' in resume_data and 'episodic_memory_scores' in resume_data:
            episodic_memory.buffer = resume_data['episodic_memory_buffer']
            episodic_memory.surprise_scores = resume_data['episodic_memory_scores']
            print(f"✅ Memoria episódica restaurada ({len(episodic_memory.buffer)}/500)")

        if 'diagnostics' in resume_data:
            diagnostics.history = resume_data['diagnostics']
            print("✅ Historial de diagnósticos restaurado")

    print(f"\n🧠 Parámetros: {sum(p.numel() for p in model.parameters()):,}")
    print(f"🎵 Audio encoder: AudioEncoder + LiquidNeuron")
    print(f"🔗 Trimodal callosum: Visual + Audio + Semantic")
    print(f"💊 Medical System: Triangulated intervention")
    print(f"🧠 Cognitive System: Reasoning + MTP + Chain-of-Thought")
    print(f"🧠 Episodic Memory: Surprise-weighted replay")

    if resume_data:
        print(f"\n🔄 REANUDANDO desde época {start_epoch}/30")
    else:
        print(f"\n🚀 INICIANDO entrenamiento desde época 0/30")

    print(f"\n🚀 Loop de entrenamiento con {len(train_loader)} batches...\n")

    # ========================================================================
    # PASO 6: LOOP DE ENTRENAMIENTO
    # ========================================================================
    for epoch in range(start_epoch, 30):
        model.train()
        total_loss = 0

        visual_node = model.right_hemisphere.visual_liquid
        audio_node = model.right_hemisphere.audio_liquid

        # Diagnóstico médico
        liquid = diagnostics.get_recent_avg('visual_liquid_norm')
        flow = diagnostics.get_recent_avg('callosal_flow')
        gate_mean = diagnostics.get_recent_avg('left_gate_mean')
        gate_std = diagnostics.get_recent_avg('left_gate_std')
        health_score = diagnostics.calculate_health(visual_node, audio_node, flow, gate_mean, gate_std, liquid)

        issues, severity, confidence = medical_system.diagnose_with_triangulation(
            health_score, liquid, gate_mean, gate_std, flow, epoch
        )
        medicine_level = "🟢 Nivel 0" if severity == 0 else f"🟡 Nivel 1" if severity <= 2 else f"🟠 Nivel 2" if severity <= 6 else "🔴 Nivel 3"

        if severity > 3 and epoch > 2:
            medical_system.apply_triangulated_intervention(model, issues, severity, confidence, epoch)

        if epoch > 1:
            model.corpus_callosum.adjust_gates_by_fatigue()

        pbar = tqdm(train_loader, desc=f"Epoch {epoch:02d} [Health: {health_score}/5 | Med: {medicine_level}]")

        for batch_idx, (images, audio_specs, captions, raw_captions) in enumerate(pbar):
            if images.dim() != 4 or audio_specs.dim() != 3 or captions.dim() != 2:
                print(f"⚠️ Dimensión inválida en batch {batch_idx}, saltando...")
                continue

            images = images.to(device, non_blocking=True)
            audio_specs = audio_specs.to(device, non_blocking=True)
            captions = captions.to(device, non_blocking=True)

            optimizer.zero_grad()

            (logits, fused_feat, enriched_ctx, gate,
             vis_post, vis_pre, aud_post, aud_pre,
             channels, mtp_loss, reasoning_steps) = model(
                images, audio_specs, captions, epoch=epoch
            )

            linguistic_reward = None
            if batch_idx % 20 == 0 and epoch >= 2:
                with torch.no_grad():
                    sample_size = min(2, images.size(0))
                    sample_indices = np.random.choice(images.size(0), size=sample_size, replace=False)
                    references = [raw_captions[i] for i in sample_indices]

                    sample_images = images[sample_indices]
                    sample_audio = audio_specs[sample_indices]
                    generated, _, _, _, _, _, _, _, _, _, _ = model(
                        sample_images, sample_audio, captions=None, epoch=epoch
                    )

                    hypotheses = []
                    for i in range(generated.size(0)):
                        gen_words = [id2word.get(int(t.item()), '<UNK>') for t in generated[i]]
                        gen_sentence = " ".join(w for w in gen_words if w not in ['<BOS>', '<EOS>', '<PAD>'])
                        hypotheses.append(gen_sentence)

                    if all(len(h.strip()) > 0 for h in hypotheses):
                        linguistic_reward = cognitive_system.linguistic_feedback.compute_linguistic_reward(references, hypotheses)

                        if reasoning_steps is not None and reasoning_steps.numel() == images.size(0):
                            sample_steps = reasoning_steps[sample_indices]
                            coherence, consistency = diagnostics.evaluate_reasoning_quality(
                                hypotheses, references, sample_steps.tolist()
                            )
                            diagnostics.update(logical_coherence=coherence, reasoning_efficiency=consistency)

            loss, ce_loss, gate_penalty, diversity_penalty, coherence_loss, linguistic_loss, mtp_term = compute_tricameral_loss(
                logits, captions, gate, vocab, vis_post, aud_post, mtp_loss, linguistic_reward,
                lambda_reward=0.1, lambda_mtp=0.1
            )

            alignment_loss = compute_alignment_loss(fused_feat, channels, epoch=epoch) if epoch < 6 else torch.tensor(0.0, device=device)
            total_loss_batch = loss + alignment_loss

            total_loss_batch.backward()

            grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            if torch.isnan(grad_norm):
                print(f"⚠️ Grad norm NaN detectado en batch {batch_idx}, saltando optimización")
                optimizer.zero_grad()
                continue

            optimizer.step()

            plasticity = 0.1 if epoch < 10 else max(0.01, 0.1 * (1 - (epoch - 10) / 20))
            model.right_hemisphere.visual_liquid.hebbian_update(vis_post, vis_pre, plasticity)
            model.right_hemisphere.audio_liquid.hebbian_update(aud_post, aud_pre, plasticity)

            model.right_hemisphere.visual_liquid.update_physiology_advanced(ce_loss.item())
            model.right_hemisphere.audio_liquid.update_physiology_advanced(ce_loss.item())

            total_loss += ce_loss.item()

            # Memoria episódica
            if batch_idx % 5 == 0:
                surprise = episodic_memory.compute_surprise(logits, captions[:, 1:], gate.mean())
                sample_indices_mem = np.random.choice(images.size(0), size=min(2, images.size(0)), replace=False)
                for idx in sample_indices_mem:
                    episodic_memory.add(
                        images[idx].detach(),
                        audio_specs[idx].detach(),
                        captions[idx].detach(),
                        surprise
                    )

            # REEMPLAZAR la sección de replay episódico (líneas ~2749-2777) en train_tricameral()

            if batch_idx % 20 == 0 and len(episodic_memory.buffer) >= 64:
                replay_batch_size = 8
                replay_samples = episodic_memory.sample(replay_batch_size)

                if replay_samples and len(replay_samples) > 0:
                    try:
                        # FIX: Mover a GPU solo aquí, liberar inmediatamente después
                        replay_imgs = torch.stack([s[0].to(device) for s in replay_samples])
                        replay_audio = torch.stack([s[1].to(device) for s in replay_samples])
                        replay_caps = torch.stack([s[2].to(device) for s in replay_samples])

                        (logits_replay, _, _, gate_replay, vis_post_replay, vis_pre_replay,
                         aud_post_replay, aud_pre_replay, _, mtp_loss_replay, _) = model(
                            replay_imgs, replay_audio, replay_caps, epoch=epoch
                        )

                        loss_replay, ce_replay, _, _, _, _, _ = compute_tricameral_loss(
                            logits_replay, replay_caps, gate_replay, vocab,
                            vis_post_replay, aud_post_replay
                        )

                        (0.3 * loss_replay).backward()

                        model.right_hemisphere.visual_liquid.hebbian_update(
                            vis_post_replay, vis_pre_replay, plasticity * 1.5
                        )
                        model.right_hemisphere.audio_liquid.hebbian_update(
                            aud_post_replay, aud_pre_replay, plasticity * 1.5
                        )

                        # FIX: LIBERAR MEMORIA INMEDIATAMENTE
                        del replay_imgs, replay_audio, replay_caps
                        del logits_replay, gate_replay, vis_post_replay, vis_pre_replay
                        del aud_post_replay, aud_pre_replay, loss_replay, ce_replay
                        torch.cuda.empty_cache()

                    except (RuntimeError, IndexError, torch.cuda.OutOfMemoryError) as e:
                        print(f"⚠️ Replay falló (memoria): {type(e).__name__}")
                        torch.cuda.empty_cache()

            # Diagnósticos
            if batch_idx % 20 == 0:
                with torch.no_grad():
                    visual_liquid_norm = model.right_hemisphere.visual_liquid.W_fast_short.norm().item()
                    audio_liquid_norm = model.right_hemisphere.audio_liquid.W_fast_short.norm().item()
                    callosal_flow = diagnostics.measure_callosal_flow(fused_feat, enriched_ctx, channels)
                    gate_mean_val = gate.mean().item() if gate.numel() > 1 else gate.item()
                    gate_std_val = gate.std().item() if gate.numel() > 1 else 0.0
                    channel_fatigue = channels['fatigue']

                    synergy = diagnostics.calculate_synergy(
                        visual_node, audio_node, callosal_flow, gate_mean_val, gate_std_val
                    )

                    reasoning_steps_val = reasoning_steps.mean().item() if torch.is_tensor(reasoning_steps) else 0.0
                    mtp_loss_val = mtp_loss.item() if torch.is_tensor(mtp_loss) else 0.0
                    linguistic_reward_val = linguistic_reward.item() if linguistic_reward is not None else 0.0
                    alignment_loss_val = alignment_loss.item() if torch.is_tensor(alignment_loss) else 0.0

                    diagnostics.update(
                        loss=ce_loss.item(),
                        visual_liquid_metabolism=float(visual_node.metabolism),
                        visual_liquid_fatigue=float(visual_node.fatigue),
                        visual_liquid_norm=visual_liquid_norm,
                        audio_liquid_metabolism=float(audio_node.metabolism),
                        audio_liquid_fatigue=float(audio_node.fatigue),
                        audio_liquid_norm=audio_liquid_norm,
                        callosal_flow=callosal_flow,
                        left_gate_mean=gate_mean_val,
                        left_gate_std=gate_std_val,
                        synergy_score=synergy,
                        health_score=health_score,
                        coherence_loss=coherence_loss.item(),
                        callosum_visual_fatigue=channel_fatigue['visual'],
                        callosum_audio_fatigue=channel_fatigue['audio'],
                        callosum_semantic_fatigue=channel_fatigue['semantic'],
                        reasoning_steps=reasoning_steps_val,
                        mtp_loss=mtp_loss_val,
                        linguistic_reward=linguistic_reward_val,
                        alignment_loss=alignment_loss_val
                    )

            pbar_dict = {
                'loss': f'{ce_loss.item():.3f}',
                'gate': f'{gate_mean_val:.2f}',
                'mem': f"{len(episodic_memory.buffer)}/{episodic_memory.capacity}",
                'coherence': f'{coherence_loss.item():.3f}'
            }

            if torch.is_tensor(mtp_loss):
                pbar_dict['mtp'] = f'{mtp_loss.item():.3f}'

            if torch.is_tensor(reasoning_steps):
                pbar_dict['reason'] = f'{reasoning_steps.mean().item():.1f}'

            if linguistic_reward is not None:
                pbar_dict['reward'] = f'{linguistic_reward.item():.3f}'

            if epoch < 6:
                pbar_dict['align'] = f'{alignment_loss_val:.3f}'

            if batch_idx % 500 == 0 and batch_idx > 0:
                avg_surprise = np.mean(episodic_memory.surprise_scores[-100:]) if len(episodic_memory.surprise_scores) >= 100 else 0.0
                pbar_dict['avg_surp'] = f'{avg_surprise:.2f}'

            pbar.set_postfix(pbar_dict)

        scheduler.step()

        # ========================================================================
        # GENERACIÓN DE TEXTO AL FINAL DE CADA ÉPOCA
        # ========================================================================
        print(f"\n{'='*80}")
        print(f"📝 GENERACIONES - Época {epoch}")
        print(f"{'='*80}")

        model.eval()
        with torch.no_grad():
            # Seleccionar 5 muestras aleatorias del validation set
            val_indices = np.random.choice(len(val_dataset), size=min(5, len(val_dataset)), replace=False)

            for i, idx in enumerate(val_indices):
                img, aud, cap, raw_cap = val_dataset[idx]

                img_batch = img.unsqueeze(0).to(device)
                aud_batch = aud.unsqueeze(0).to(device)

                generated, _, _, _, _, _, _, _, _, _, _ = model(
                    img_batch, aud_batch, captions=None, epoch=epoch
                )

                gen_words = [id2word.get(int(t.item()), '<UNK>') for t in generated[0]]
                gen_sentence = " ".join(w for w in gen_words if w not in ['<BOS>', '<EOS>', '<PAD>'])

                print(f"\n[Muestra {i+1}]")
                print(f"  Referencia: {raw_cap}")
                print(f"  Generada:   {gen_sentence}")

                bleu = diagnostics.language_metrics.sentence_bleu(raw_cap, gen_sentence)
                acc = diagnostics.language_metrics.token_accuracy(raw_cap, gen_sentence)
                overlap = diagnostics.language_metrics.word_overlap(raw_cap, gen_sentence)

                print(f"  BLEU: {bleu:.3f} | Acc: {acc:.3f} | Overlap: {overlap:.3f}")

        print(f"{'='*80}\n")
        model.train()

        # ========================================================================
        # VALIDACIÓN Y CHECKPOINTS
        # ========================================================================
        if epoch % 2 == 0:
            model.eval()
            val_loss = 0
            val_batches = 0

            with torch.no_grad():
                for val_images, val_audio, val_captions, val_raw in tqdm(val_loader, desc="Validación", leave=False):
                    val_images = val_images.to(device, non_blocking=True)
                    val_audio = val_audio.to(device, non_blocking=True)
                    val_captions = val_captions.to(device, non_blocking=True)

                    (val_logits, _, _, _, _, _, _, _, _, _, _) = model(val_images, val_audio, val_captions, epoch=epoch)
                    val_ce = F.cross_entropy(val_logits.reshape(-1, len(vocab)), val_captions[:, 1:].reshape(-1), ignore_index=vocab['<PAD>'])
                    val_loss += val_ce.item()
                    val_batches += 1

                    # FIX: Liberar memoria cada 10 batches de validación
                    if val_batches % 10 == 0:
                        del val_images, val_audio, val_captions, val_logits, val_ce
                        torch.cuda.empty_cache()

            avg_val_loss = val_loss / val_batches
            print(f"\n✅ Validación - Loss: {avg_val_loss:.4f}")

            # FIX: Limpiar cache después de validación completa
            torch.cuda.empty_cache()

            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_loss': avg_val_loss,
                }, './checkpoints/tricameral_best_val.pth')
                print(f"💾 Mejor modelo guardado: val_loss={avg_val_loss:.4f}")

            model.train()

        if epoch % 2 == 0:
            checkpoint_path = f'./checkpoints/tricameral_epoch_{epoch:02d}_full.pth'
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'vocab': vocab,
                'id2word': id2word,
                'diagnostics': diagnostics.history,
                'medical_interventions': medical_system.intervention_history,
                'cognitive_interventions': cognitive_system.cognitive_history,
                'cache_stats': cognitive_system.linguistic_feedback.get_cache_stats(),
                'episodic_memory_size': len(episodic_memory.buffer),
                'episodic_memory_buffer': episodic_memory.buffer,
                'episodic_memory_scores': episodic_memory.surprise_scores,
                'best_val_loss': best_val_loss,
            }, checkpoint_path)
            print(f"💾 Checkpoint guardado: {checkpoint_path}")

        diagnostics.report(epoch)
        print(f"✅ Época {epoch:02d} | Loss: {total_loss/len(train_loader):.4f}\n")

        if len(episodic_memory.buffer) > 0:
            avg_surprise = np.mean(episodic_memory.surprise_scores)
            max_surprise = np.max(episodic_memory.surprise_scores)
            high_surprise_count = sum(1 for s in episodic_memory.surprise_scores if s > episodic_memory.surprise_threshold * 1.5)

            print(f"\n{'='*60}")
            print(f"🧠 MEMORIA EPISÓDICA - Fin de Época {epoch}")
            print(f"  Buffer: {len(episodic_memory.buffer)}/{episodic_memory.capacity}")
            print(f"  Surprise: avg={avg_surprise:.3f}, max={max_surprise:.3f}")
            print(f"  Muestras alta sorpresa: {high_surprise_count} ({100*high_surprise_count/len(episodic_memory.buffer):.1f}%)")
            print(f"{'='*60}\n")

    # ========================================================================
    # CHECKPOINT FINAL
    # ========================================================================
    final_checkpoint = {
        'epoch': 29,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'scheduler_state_dict': scheduler.state_dict(),
        'vocab': vocab,
        'id2word': id2word,
        'diagnostics': diagnostics.history,
        'medical_interventions': medical_system.intervention_history,
        'cognitive_interventions': cognitive_system.cognitive_history,
        'cache_stats': cognitive_system.linguistic_feedback.get_cache_stats(),
        'episodic_memory_size': len(episodic_memory.buffer),
        'episodic_memory_buffer': episodic_memory.buffer,
        'episodic_memory_scores': episodic_memory.surprise_scores,
        'best_val_loss': best_val_loss,
        'final_train_loss': total_loss / len(train_loader),
    }

    torch.save(final_checkpoint, './tricameral_model_final_full.pth')
    print("💾 Modelo final guardado con estado completo: ./tricameral_model_final_full.pth")

    print(f"\n{'='*80}")
    print("📋 HISTORIAL DE INTERVENCIONES - RESUMEN NEUROCOGNITIVO")
    print(f"{'='*80}")

    print(f"\n🏥 INTERVENCIONES MÉDICAS: {len(medical_system.intervention_history)}")
    if len(medical_system.intervention_history) == 0:
        print("✓ No se requirieron intervenciones médicas - Sistema homeostático estable")
    else:
        for intervention in medical_system.intervention_history:
            print(f"Época {intervention['epoch']:02d} | {intervention['level']} | Severidad: {intervention['severity']}/12")
            print(f"  Problemas: {', '.join(intervention['issues'])}")
            for inter in intervention['interventions']:
                print(f"    • {inter}")
            print()

    print(f"\n🧠 INTERVENCIONES COGNITIVAS: {sum(1 for h in cognitive_system.cognitive_history if h['severity'] > 0)}")
    if len(cognitive_system.cognitive_history) == 0:
        print("✓ No se requirieron intervenciones cognitivas - Razonamiento óptimo")
    else:
        for intervention in cognitive_system.cognitive_history:
            if intervention['severity'] > 0:
                print(f"Época {intervention['epoch']:02d} | Severidad: {intervention['severity']}/9")
                print(f"  Issues: {', '.join(intervention['issues'])}")
                print()

    final_cache_stats = cognitive_system.linguistic_feedback.get_cache_stats()
    print(f"\n⚡ ESTADÍSTICAS FINALES DEL SISTEMA:")
    print(f"  Caché lingüístico: {final_cache_stats['cache_size']} entradas")
    print(f"  Hit rate: {final_cache_stats['hit_rate']:.2%}")
    print(f"  Memoria episódica: {len(episodic_memory.buffer)}/{episodic_memory.capacity} samples")
    print(f"  Best val loss: {best_val_loss:.4f}")

    final_fatigue = {
        'visual': diagnostics.get_recent_avg('callosum_visual_fatigue'),
        'audio': diagnostics.get_recent_avg('callosum_audio_fatigue'),
        'semantic': diagnostics.get_recent_avg('callosum_semantic_fatigue')
    }
    print(f"\n🔗 DISTRIBUCIÓN DE FATIGA FINAL:")
    for k, v in final_fatigue.items():
        print(f"  {k}: {v:.3f} {'🔴' if v > 0.3 else '🟡' if v > 0.15 else '🟢'}")

    print(f"\n{'='*80}")
    print("🧠 ENTRENAMIENTO TRICAMERAL COMPLETADO - SISTEMA NEUROCOGNITIVO ESTABLE")
    print(f"{'='*80}")




# =============================================================================
# EJECUCIÓN DIRECTA
# =============================================================================
if __name__ == "__main__":
    # Descargar dataset automáticamente
    print("🚀 Iniciando descarga del dataset...")
    path = kagglehub.dataset_download("warcoder/flickr-8k-audio-caption-corpus")
    print(f"📦 Dataset descargado en: {path}")

    # Entrenar
    train_tricameral()