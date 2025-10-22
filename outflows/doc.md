# Documentação do App `outflows`

Este documento detalha a estrutura e o funcionamento do aplicativo `outflows` dentro do Sistema de Gerenciamento de Estoque (SGE). O objetivo deste app é gerenciar o registro de saídas de produtos do estoque, seja por venda, perda, dano ou ajuste.

## 1. Model (`models.py`)

O coração do app é o modelo `Outflow`, que representa uma transação de saída de produto.

### `Outflow`

| Campo          | Tipo                  | Descrição                                       | Opções                                                                                             |
| :------------- | :-------------------- | :---------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `product`      | `ForeignKey(Product)` | O produto que está saindo do estoque.           | Obrigatório, `on_delete=models.PROTECT`, `verbose_name="Produto"`                                  |
| `quantity`     | `IntegerField`        | A quantidade de itens que saíram.               | Obrigatório, `verbose_name="Quantidade"`                                                           |
| `outflow_type` | `CharField(20)`       | O tipo de saída (Venda, Perda, Ajuste, etc.).   | Obrigatório, `choices=OUTFLOW_TYPE_CHOICES`, `verbose_name="Tipo de Saída"`                        |
| `invoice_number`| `CharField(50)`      | Número da nota fiscal da venda (se aplicável).  | Opcional, `verbose_name="Nota Fiscal"`                                                             |
| `user`         | `ForeignKey(User)`    | O usuário que registrou a saída.                | Opcional (`null=True`), `on_delete=models.SET_NULL`, `verbose_name="Usuário"`                      |
| `description`  | `TextField`           | Descrição ou observações sobre a saída.         | Opcional, `verbose_name="Descrição"`                                                               |
| `created_at`   | `DateTimeField`       | Data e hora de criação do registro.             | `auto_now_add=True`, `verbose_name="Data da Saída"`                                                |
| `updated_at`   | `DateTimeField`       | Data e hora da última atualização do registro.  | `auto_now=True`, `verbose_name="Atualizado em"`                                                    |

**Meta Opções:**
- `verbose_name`: 'Saída'
- `verbose_name_plural`: 'Saídas'
- `ordering`: ['-created_at'] (As listagens são ordenadas pela data de criação, da mais recente para a mais antiga).

**Relações:**
- **Produto (`Product`):** Uma saída está sempre ligada a um produto. A exclusão de um produto é impedida (`PROTECT`) se houver saídas associadas a ele.
- **Usuário (`User`):** Registra qual usuário realizou a operação. Se o usuário for excluído, o campo fica nulo (`SET_NULL`).

---

## 2. Views (`views.py`)

As views são baseadas em classes (Class-Based Views) do Django e exigem que o usuário esteja logado (`LoginRequiredMixin`).

### `OutflowListView`
- **Tipo:** `ListView`
- **Função:** Lista todas as saídas de estoque, com paginação de 10 itens por página.
- **Template:** `outflow_list.html`
- **Contexto:** A lista de saídas é injetada no template com o nome `object_list`.
- **Funcionalidade Extra:** Suporta busca por título do produto ou número da nota fiscal.

### `OutflowCreateView`
- **Tipo:** `CreateView`
- **Função:** Exibe um formulário para registrar uma nova saída de produto.
- **Template:** `outflow_create.html`
- **Formulário:** `OutflowForm`
- **Sucesso:** Após o registro, redireciona para a URL `outflows_list`.
- **Lógica Adicional:** O campo `user` é preenchido automaticamente com o usuário logado no momento do envio do formulário.

### `OutflowDetailView`
- **Tipo:** `DetailView`
- **Função:** Exibe os detalhes de uma saída específica.
- **Template:** `outflow_detail.html`
- **Contexto:** O objeto da saída é injetado no template com o nome `outflow`.

---

## 3. URLs (`urls.py`)

As URLs mapeiam os caminhos da web para as views correspondentes.

| URL Path                    | View                 | Nome da URL (`name`) | Descrição                               |
| :-------------------------- | :------------------- | :------------------- | :-------------------------------------- |
| `outflows/list/`            | `OutflowListView`    | `outflows_list`      | Lista todas as saídas.                  |
| `outflows/create/`          | `OutflowCreateView`  | `outflows_create`    | Exibe o formulário de registro de saída. |
| `outflows/<int:pk>/detail/` | `OutflowDetailView`  | `outflows_detail`    | Mostra os detalhes de uma saída.        |

---

## 4. Forms (`forms.py`)

Os formulários são usados para registrar novas instâncias do modelo `Outflow`.

### `OutflowForm`
- **Tipo:** `ModelForm`
- **Modelo Associado:** `Outflow`
- **Campos:** `product`, `quantity`, `outflow_type`, `invoice_number`, `description`.
- **Validação Customizada:**
  - `clean_quantity()`: Verifica se a quantidade de saída não é maior que a quantidade disponível em estoque para o produto selecionado.
- **Widgets Customizados:** (Inferido com base em outros apps)
  - `product`: `forms.Select` com a classe `form-control`.
  - `quantity`: `forms.NumberInput` com a classe `form-control`.
  - `outflow_type`: `forms.Select` com a classe `form-control`.
  - `invoice_number`: `forms.TextInput` com a classe `form-control`.
  - `description`: `forms.Textarea` com a classe `form-control`.

---

## 5. Templates

- **`outflow_list.html`**: Página principal que exibe o histórico de saídas em uma tabela. Inclui um formulário de busca, um botão para criar uma "Nova Saída" e um botão de ação (detalhe) para cada item. Também inclui o componente de paginação e cartões com métricas (Quantidade de Vendas, Produtos Vendidos, etc.).
- **`outflow_create.html`**: (Inferido) Contém o formulário para registrar uma nova saída de produto.
- **`outflow_detail.html`**: (Inferido) Exibe todas as informações de uma única saída em modo de leitura.

---

## 6. Admin (`admin.py`)

Para uma melhor experiência de gerenciamento no Django Admin, uma configuração `OutflowAdmin` pode ser criada e registrada.

### `OutflowAdmin` (Sugestão)
- **`list_display`**: `product`, `quantity`, `outflow_type`, `user`, `created_at`, `invoice_number`.
- **`search_fields`**: `product__title`, `invoice_number`, `user__username`.
- **`list_filter`**: `outflow_type`, `product`, `user`, `created_at`.
- **`autocomplete_fields`**: `product`, `user`.
- **`fieldsets`**: Organização do formulário de edição em seções lógicas para melhor visualização.