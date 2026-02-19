# Exome + Vue

Use `useStore` from `exome/vue` in `<script setup>` for reactive state.

```vue
<script setup>
import { useStore } from 'exome/vue';
import { counter } from './counter.store';

const { count, increment, decrement } = useStore(counter);
</script>

<template>
  <h1>{{ count }}</h1>
  <button @click="decrement">-</button>
  <button @click="increment">+</button>
</template>
```
