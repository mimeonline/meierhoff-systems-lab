<script setup>
import { computed } from 'vue'
import { useNav } from '@slidev/client'

const { currentSlideRoute } = useNav()
const chapter = computed(() => currentSlideRoute.value?.meta?.slide?.frontmatter?.chapter)
</script>

<template>
  <Transition name="chapter-fade">
    <div v-if="chapter" class="chapter-badge" :key="chapter">
      {{ chapter }}
    </div>
  </Transition>
</template>

<style scoped>
.chapter-badge {
  position: absolute;
  top: 1.1rem;
  right: 1.4rem;
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--msl-accent-light);
  background: rgba(56, 139, 210, 0.08);
  border: 1px solid rgba(56, 139, 210, 0.2);
  border-radius: 20px;
  padding: 0.28rem 0.8rem;
  z-index: 100;
  pointer-events: none;
  white-space: nowrap;
}

.chapter-fade-enter-active,
.chapter-fade-leave-active {
  transition: opacity 0.25s ease;
}
.chapter-fade-enter-from,
.chapter-fade-leave-to {
  opacity: 0;
}
</style>
