# Exome + Lit

Use `exomeLitMixin` from `exome/lit` to make a LitElement reactive to store changes.

```ts
import { LitElement, html } from 'lit';
import { customElement } from 'lit/decorators.js';
import { exomeLitMixin } from 'exome/lit';
import { counter } from './counter.store';

@customElement('my-counter')
class MyCounter extends exomeLitMixin(LitElement, [counter]) {
  render() {
    return html`
      <h1>${counter.count}</h1>
      <button @click=${() => counter.decrement()}>-</button>
      <button @click=${() => counter.increment()}>+</button>
    `;
  }
}
```

Pass an array of stores to `exomeLitMixin` — the element re-renders when any of them change.
