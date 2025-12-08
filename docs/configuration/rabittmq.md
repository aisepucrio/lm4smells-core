

## 🐰 RabbitMQ

### 📨 Exchange Configuration — `solicitacoes_exchange`

| **Parameter** | **Value** | **Description** |
|----------------|------------|-----------------|
| **Name** | `solicitacoes_exchange` | Identifier of the exchange, used for message routing. |
| **Type** | `direct` | Defines routing type. In `direct`, messages are delivered to queues with a *binding key* that exactly matches the *routing key* used when publishing. |
| **Durability** | `Durable` | The exchange persists even after the broker restarts (non-volatile). |
| **Auto Delete** | `No` | The exchange **will not** be automatically deleted when it is no longer in use. |
| **Internal** | `No` | Can be used by external producers and consumers. |
| **Arguments** | *(none)* | No additional arguments configured. Can be used for advanced parameters (e.g., TTL, DLX, etc.). |
| **Alternate Exchange** | *(not configured)* | No alternate exchange associated. |

---

### 🧭 Example Binding

| **Queue** | **Routing Key** | **Description** |
|------------|-----------------|-----------------|
| `python-smell` | `python-smell` | Receives messages routed from the `solicitacoes_exchange` exchange when the routing key matches. |

---

### 📨 Exchange Binding Information

| **From**               | **Routing Key** | **Arguments** |
| ----------------------- | --------------- | -------------- |
| (Default exchange binding) | `python-smell`  | —              |
| `solicitacoes_exchange`    | `python-smell`  | —              |


