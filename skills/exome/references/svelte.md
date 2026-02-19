# Exome + Svelte

Use `useStore` from `exome/svelte` with an optional selector to create reactive variables.

```svelte
<script>
import { useStore } from 'exome/svelte';
import { counter } from './counter.store';

const count = useStore(counter, s => s.count);
</script>

<h1>{$count}</h1>
<button on:click={() => counter.decrement()}>-</button>
<button on:click={() => counter.increment()}>+</button>
```
