# Exome + RxJS

Use `observeStore` from `exome/rxjs` to get an observable that emits on store changes.

```ts
import { observeStore } from 'exome/rxjs';
import { map } from 'rxjs';
import { counter } from './counter.store';

const count$ = observeStore(counter).pipe(
  map(store => store.count)
);

count$.subscribe(count => console.log(count));
```
