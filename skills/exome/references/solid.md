# Exome + Solid

Use `useStore` from `exome/solid` for reactive access.

```tsx
import { useStore } from 'exome/solid';
import { counter } from './counter.store';

function Counter() {
  const store = useStore(counter);
  return (
    <div>
      <h1>{store.count}</h1>
      <button onClick={() => counter.decrement()}>-</button>
      <button onClick={() => counter.increment()}>+</button>
    </div>
  );
}
```
