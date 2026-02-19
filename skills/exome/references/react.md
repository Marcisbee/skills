# Exome + React/Preact

Import `useStore` from `exome/react` (or `exome/preact`). It returns reactive state and bound actions.

```tsx
import { useStore } from 'exome/react';
import { getExomeId } from 'exome';

function Counter() {
  const { count, increment, decrement } = useStore(counter);
  return (
    <div>
      <h1>{count}</h1>
      <button onClick={decrement}>-</button>
      <button onClick={increment}>+</button>
    </div>
  );
}
```

## Nested Stores

Pass child store instances to `useStore` in child components:

```tsx
function Todo({ todo }: { todo: TodoStore }) {
  const { content, completed, toggle } = useStore(todo);
  return (
    <label>
      <input type="checkbox" checked={completed} onChange={toggle} />
      {content}
    </label>
  );
}

function TodoList() {
  const { filteredTodos, addTodo } = useStore(todoList);
  return (
    <ul>
      {filteredTodos.map(todo => (
        <li key={getExomeId(todo)}>
          <Todo todo={todo} />
        </li>
      ))}
    </ul>
  );
}
```

Use `getExomeId(store)` for stable React keys when rendering store lists.
