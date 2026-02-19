# Exome + Angular

Use `useStore` from `exome/angular` to get a reactive store reference in components.

```ts
import { Component } from '@angular/core';
import { useStore } from 'exome/angular';
import { counter } from './counter.store';

@Component({
  selector: 'app-counter',
  template: `
    <h1>{{ store.count }}</h1>
    <button (click)="store.decrement()">-</button>
    <button (click)="store.increment()">+</button>
  `,
})
export class CounterComponent {
  store = useStore(counter);
}
```
