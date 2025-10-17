# Documentação do App `suppliers`

Este documento detalha a estrutura e o funcionamento do aplicativo `suppliers` dentro do Sistema de Gerenciamento de Estoque (SGE). O objetivo deste app é gerenciar os fornecedores de produtos do sistema.

## 1. Model (`models.py`)

O coração do app é o modelo `Supplier`, que representa um fornecedor de produtos.

### `Supplier`

| Campo | Tipo | Descrição | Opções |
| :--- | :--- | :--- | :--- |
| `name` | `CharField(255)` | Nome do fornecedor. | Obrigatório, `verbose_name="Nome"` |
| `cnpj` | `CharField(18)` | CNPJ do fornecedor. | Opcional, Único, `verbose_name="CNPJ"` |
| `email` | `EmailField(255)` | E-mail de contato. | Opcional, `verbose_name="E-mail"` |
| `phone` | `CharField(20)` | Telefone de contato. | Opcional, `verbose_name="Telefone"` |
| `address` | `TextField` | Endereço do fornecedor. | Opcional, `verbose_name="Endereço"` |
| `description` | `TextField` | Descrição ou observações sobre o fornecedor. | Opcional, `verbose_name="Descrição"` |
| `created_at` | `DateTimeField` | Data de criação do registro. | `auto_now_add=True` |
| `updated_at` | `DateTimeField` | Data da última atualização. | `auto_now=True` |

**Meta Opções:**
- `verbose_name`: 'Fornecedor'
- `verbose_name_plural`: 'Fornecedores'
- `ordering`: ['name'] (As listagens são ordenadas pelo nome do fornecedor por padrão).

**Relações:**
- **Entrada (`Inflow`):** Um fornecedor pode estar associado a várias entradas de estoque. A relação é definida no modelo `Inflow` com `on_delete=models.PROTECT`, o que impede que um fornecedor seja excluído se houver entradas de estoque associadas a ele.

---

## 2. Views (`views.py`)

As views são baseadas em classes (Class-Based Views) do Django, facilitando a implementação das operações de CRUD (Create, Read, Update, Delete).

### `SupplierListView`
- **Tipo:** `ListView`
- **Função:** Lista todos os fornecedores cadastrados, com paginação.
- **Template:** `supplier_list.html`
- **Contexto:** A lista de fornecedores é injetada no template com o nome `suppliers`.
- **Funcionalidade Extra:** Suporta busca por nome através de um parâmetro GET `name`. A busca filtra fornecedores cujo nome contém o texto fornecido (case-insensitive).

### `SupplierCreateView`
- **Tipo:** `CreateView`
- **Função:** Exibe um formulário para criar um novo fornecedor.
- **Template:** `supplier_create.html`
- **Formulário:** `SupplierForm`
- **Sucesso:** Após a criação, redireciona para a URL `supplier_list`.

### `SupplierDetailView`
- **Tipo:** `DetailView`
- **Função:** Exibe os detalhes de um fornecedor específico.
- **Template:** `supplier_detail.html`
- **Contexto:** O objeto do fornecedor é injetado no template com o nome `supplier`.

### `SupplierUpdateView`
- **Tipo:** `UpdateView`
- **Função:** Exibe um formulário preenchido com os dados de um fornecedor existente para edição.
- **Template:** `supplier_update.html`
- **Formulário:** `SupplierForm`
- **Sucesso:** Após a atualização, redireciona para a URL `supplier_list`.

### `SupplierDeleteView`
- **Tipo:** `DeleteView`
- **Função:** Exibe uma página de confirmação antes de excluir um fornecedor.
- **Template:** `supplier_delete.html`
- **Sucesso:** Após a exclusão, redireciona para a URL `supplier_list`.

---

## 3. URLs (`urls.py`)

As URLs mapeiam os caminhos da web para as views correspondentes.

| URL Path | View | Nome da URL (`name`) | Descrição |
| :--- | :--- | :--- | :--- |
| `suppliers/list/` | `SupplierListView` | `supplier_list` | Lista todos os fornecedores. |
| `suppliers/create/` | `SupplierCreateView` | `supplier_create` | Exibe o formulário de criação de fornecedor. |
| `suppliers/<int:pk>/detail/` | `SupplierDetailView` | `supplier_detail` | Mostra os detalhes de um fornecedor. |
| `suppliers/<int:pk>/update/` | `SupplierUpdateView` | `supplier_update` | Permite editar um fornecedor existente. |
| `suppliers/<int:pk>/delete/` | `SupplierDeleteView` | `supplier_delete` | Permite excluir um fornecedor. |

---

## 4. Forms (`forms.py`)

Os formulários são usados para criar e atualizar instâncias do modelo `Supplier`.

### `SupplierForm`
- **Tipo:** `ModelForm`
- **Modelo Associado:** `Supplier`
- **Campos:** `name`, `cnpj`, `email`, `phone`, `address`, `description`.
- **Validação Customizada:**
  - `clean_cnpj()`: Remove a máscara do CNPJ e valida se o campo contém 14 dígitos.
- **Widgets Customizados:** Todos os campos são estilizados com a classe `form-control`. `address` e `description` usam `Textarea`. Campos como `cnpj`, `email` e `phone` possuem `placeholders` para guiar o usuário.

---

## 5. Templates

- **`supplier_list.html`**: Página principal que exibe a lista de fornecedores em uma tabela. Inclui um formulário de busca, um botão para criar um novo fornecedor e botões de ação (detalhe, editar, excluir) para cada item. Também inclui o componente de paginação.
- **`supplier_create.html`**: Contém o formulário para adicionar um novo fornecedor.
- **`supplier_update.html`**: Contém o formulário para editar um fornecedor existente.
- **`supplier_detail.html`**: Exibe todas as informações de um único fornecedor em modo de leitura.
- **`supplier_delete.html`**: Página de confirmação para a exclusão de um fornecedor. Apresenta uma mensagem de alerta e botões para confirmar ou cancelar a ação.

