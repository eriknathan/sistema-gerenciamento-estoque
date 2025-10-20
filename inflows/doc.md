# Documentação do App `inflows`

Este documento detalha a estrutura e o funcionamento do aplicativo `inflows` dentro do Sistema de Gerenciamento de Estoque (SGE). O objetivo deste app é gerenciar o registro de entradas de produtos no estoque.

## 1. Model (`models.py`)

O coração do app é o modelo `Inflow`, que representa uma transação de entrada de produto.

### `Inflow`

| Campo            | Tipo                  | Descrição                                       | Opções                                                                                             |
| :--------------- | :-------------------- | :---------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `product`        | `ForeignKey(Product)` | O produto que está sendo adicionado ao estoque. | Obrigatório, `on_delete=models.CASCADE`, `verbose_name="Produto"`                                  |
| `supplier`       | `ForeignKey(Supplier)`| O fornecedor do produto.                        | Obrigatório, `on_delete=models.PROTECT`, `verbose_name="Fornecedor"`                               |
| `quantity`       | `IntegerField`        | A quantidade de itens que entraram.             | Obrigatório, `verbose_name="Quantidade"`                                                           |
| `invoice_number` | `CharField(50)`       | Número da nota fiscal da compra.                | Opcional, `verbose_name="Nota Fiscal"`                                                             |
| `user`           | `ForeignKey(User)`    | O usuário que registrou a entrada.              | Opcional (`null=True`), `on_delete=models.SET_NULL`, `verbose_name="Usuário"`                      |
| `description`    | `TextField`           | Descrição ou observações sobre a entrada.       | Opcional, `verbose_name="Descrição"`                                                               |
| `created_at`     | `DateTimeField`       | Data e hora de criação do registro.             | `auto_now_add=True`, `verbose_name="Data da Entrada"`                                              |
| `updated_at`     | `DateTimeField`       | Data e hora da última atualização do registro.  | `auto_now=True`, `verbose_name="Atualizado em"`                                                    |

**Meta Opções:**
- `verbose_name`: 'Entrada'
- `verbose_name_plural`: 'Entradas'
- `ordering`: ['-created_at'] (As listagens são ordenadas pela data de criação, da mais recente para a mais antiga).

**Relações:**
- **Produto (`Product`):** Uma entrada está sempre ligada a um produto. Se o produto for excluído, todas as suas entradas também serão (`CASCADE`).
- **Fornecedor (`Supplier`):** Uma entrada está ligada a um fornecedor. A exclusão de um fornecedor é impedida (`PROTECT`) se houver entradas associadas a ele.
- **Usuário (`User`):** Registra qual usuário realizou a operação. Se o usuário for excluído, o campo fica nulo (`SET_NULL`).

---

## 2. Views (`views.py`)

As views são baseadas em classes (Class-Based Views) do Django para implementar as operações de CRUD.

### `InflowListView`
- **Tipo:** `ListView`
- **Função:** Lista todas as entradas de estoque, com paginação.
- **Template:** `inflow_list.html`
- **Contexto:** A lista de entradas é injetada no template com o nome `inflows`.
- **Funcionalidade Extra:** Suporta busca por nome do produto, nome do fornecedor ou número da nota fiscal.

### `InflowCreateView`
- **Tipo:** `CreateView`
- **Função:** Exibe um formulário para registrar uma nova entrada de produto.
- **Template:** `inflow_create.html`
- **Formulário:** `InflowForm`
- **Sucesso:** Após o registro, redireciona para a URL `inflow_list`.

### `InflowDetailView`
- **Tipo:** `DetailView`
- **Função:** Exibe os detalhes de uma entrada específica.
- **Template:** `inflow_detail.html`
- **Contexto:** O objeto da entrada é injetado no template com o nome `inflow`.

### `InflowDeleteView`
- **Tipo:** `DeleteView`
- **Função:** Exibe uma página de confirmação antes de excluir uma entrada. A exclusão de uma entrada deve reverter a adição da quantidade no estoque do produto associado.
- **Template:** `inflow_delete.html`
- **Sucesso:** Após a exclusão, redireciona para a URL `inflow_list`.

---

## 3. URLs (`urls.py`)

As URLs mapeiam os caminhos da web para as views correspondentes.

| URL Path                  | View                 | Nome da URL (`name`) | Descrição                               |
| :------------------------ | :------------------- | :------------------- | :-------------------------------------- |
| `inflows/list/`           | `InflowListView`     | `inflow_list`        | Lista todas as entradas.                |
| `inflows/create/`         | `InflowCreateView`   | `inflow_create`      | Exibe o formulário de registro de entrada. |
| `inflows/<int:pk>/detail/`| `InflowDetailView`   | `inflow_detail`      | Mostra os detalhes de uma entrada.      |
| `inflows/<int:pk>/delete/`| `InflowDeleteView`   | `inflow_delete`      | Permite excluir uma entrada.            |

---

## 4. Forms (`forms.py`)

Os formulários são usados para registrar novas instâncias do modelo `Inflow`.

### `InflowForm`
- **Tipo:** `ModelForm`
- **Modelo Associado:** `Inflow`
- **Campos:** `product`, `supplier`, `quantity`, `invoice_number`, `description`.
- **Widgets Customizados:**
  - `product`, `supplier`: `forms.Select` com a classe `form-control`.
  - `quantity`: `forms.NumberInput` com a classe `form-control`.
  - `invoice_number`: `forms.TextInput` com a classe `form-control`.
  - `description`: `forms.Textarea` com a classe `form-control`.

---

## 5. Admin (`admin.py`)

A integração com o Django Admin permite o gerenciamento das entradas diretamente pela interface administrativa, com várias melhorias para usabilidade.

### `InflowAdmin`
- **`list_display`**: Exibe as colunas `product`, `quantity`, `supplier`, `user`, `created_at`, `invoice_number`.
- **`search_fields`**: Permite a busca por `product__title`, `supplier__name`, `invoice_number` e `user__username`.
- **`list_filter`**: Adiciona filtros na barra lateral para `supplier`, `product`, `user` e `created_at`.
- **`autocomplete_fields`**: Otimiza a seleção de `product`, `supplier` e `user` com campos de busca, melhorando a performance em bancos de dados grandes.
- **`fieldsets`**: Organiza o formulário de edição em seções lógicas para melhor visualização.