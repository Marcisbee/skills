# Exome + Vanilla JS

Use `subscribe` from the core `exome` package for manual subscriptions.

```ts
import { subscribe } from 'exome';
import { counter } from './counter.store';

const unsubscribe = subscribe(counter, () => {
  document.getElementById('count')!.textContent = String(counter.count);
});
```

Returns an unsubscribe function for cleanup.
