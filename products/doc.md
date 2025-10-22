# Documentação do App `products`

Este documento detalha a estrutura e o funcionamento do aplicativo `products` dentro do Sistema de Gerenciamento de Estoque (SGE). O objetivo deste app é gerenciar o cadastro e o controle dos produtos em estoque.

## 1. Model (`models.py`)

O coração do app é o modelo `Product`, que representa um item no estoque.

### `Product`

| Campo           | Tipo                  | Descrição                                           | Opções                                                                                             |
| :-------------- | :-------------------- | :-------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `title`         | `CharField`           | Nome ou título do produto.                          | Obrigatório, `verbose_name="Título"`                                                               |
| `category`      | `ForeignKey(Category)`| A categoria à qual o produto pertence.              | Obrigatório, `on_delete=models.PROTECT`, `verbose_name="Categoria"`                                |
| `brand`         | `ForeignKey(Brand)`   | A marca do produto.                                 | Obrigatório, `on_delete=models.PROTECT`, `verbose_name="Marca"`                                    |
| `description`   | `TextField`           | Descrição detalhada do produto.                     | Opcional, `verbose_name="Descrição"`                                                               |
| `serial_number` | `CharField`           | Número de série ou código único do produto.         | Opcional, Único, `verbose_name="Número de Série"`                                                  |
| `cost_price`    | `DecimalField`        | Preço de custo do produto.                          | Obrigatório, `max_digits=10`, `decimal_places=2`, `verbose_name="Preço de Custo"`                  |
| `sale_price`    | `DecimalField`        | Preço de venda do produto.                          | Obrigatório, `max_digits=10`, `decimal_places=2`, `verbose_name="Preço de Venda"`                  |
| `quantity`      | `IntegerField`        | Quantidade atual em estoque.                        | Padrão: `0`, `verbose_name="Quantidade em Estoque"`                                                |
| `created_at`    | `DateTimeField`       | Data e hora de criação do registro.                 | `auto_now_add=True`, `verbose_name="Criado em"` (Inferido)                                         |
| `updated_at`    | `DateTimeField`       | Data e hora da última atualização do registro.      | `auto_now=True`, `verbose_name="Atualizado em"` (Inferido)                                         |

**Meta Opções:**
- `verbose_name`: 'Produto'
- `verbose_name_plural`: 'Produtos'
- `ordering`: ['title'] (As listagens são ordenadas pelo título do produto por padrão).

**Relações:**
- **Categoria (`Category`):** Um produto pertence a uma categoria. A exclusão de uma categoria é impedida (`PROTECT`) se houver produtos associados a ela.
- **Marca (`Brand`):** Um produto pertence a uma marca. A exclusão de uma marca é impedida (`PROTECT`) se houver produtos associados a ela.
- **Entrada (`Inflow`):** Um produto pode ter várias entradas de estoque.
- **Saída (`Outflow`):** Um produto pode ter várias saídas de estoque.

---

## 2. Views (`views.py`)

As views são baseadas em classes (Class-Based Views) do Django e implementam as operações de CRUD (Create, Read, Update, Delete).

### `ProductListView`
- **Tipo:** `ListView`
- **Função:** Lista todos os produtos cadastrados, com paginação de 10 itens por página.
- **Template:** `product_list.html`
- **Contexto:** A lista de produtos é injetada no template com o nome `Products`.
- **Funcionalidade Extra:**
  - Suporta busca por `title` (título do produto) e `serie_number` (número de série).
  - Permite filtrar por `category_id` e `brand_id`.
  - Adiciona listas de `categories` e `brands` ao contexto para popular os filtros dropdown.
  - Calcula e adiciona métricas ao contexto: `total_products_count` (soma das quantidades), `total_stock_cost` (custo total do estoque), `total_stock_value` (valor total de venda do estoque) e `total_stock_profit` (lucro potencial do estoque).

### `ProductCreateView`
- **Tipo:** `CreateView`
- **Função:** Exibe um formulário para registrar um novo produto.
- **Template:** `product_create.html`
- **Formulário:** `ProductForm`
- **Sucesso:** Após o registro, redireciona para a URL `product_list`.

### `ProductDetailView`
- **Tipo:** `DetailView`
- **Função:** Exibe os detalhes de um produto específico.
- **Template:** `product_detail.html`
- **Contexto:** O objeto do produto é injetado no template com o nome `Products` (singular `Product` seria mais comum).

### `ProductUpdateView`
- **Tipo:** `UpdateView`
- **Função:** Exibe um formulário preenchido com os dados de um produto existente para edição.
- **Template:** `product_update.html`
- **Formulário:** `ProductForm`
- **Sucesso:** Após a atualização, redireciona para a URL `product_list`.

### `ProductDeleteView`
- **Tipo:** `DeleteView`
- **Função:** Exibe uma página de confirmação antes de excluir um produto.
- **Template:** `product_delete.html`
- **Sucesso:** Após a exclusão, redireciona para a URL `product_list`.

---

## 3. URLs (`urls.py`)

As URLs mapeiam os caminhos da web para as views correspondentes.

| URL Path                    | View                  | Nome da URL (`name`) | Descrição                               |
| :-------------------------- | :-------------------- | :------------------- | :-------------------------------------- |
| `products/list/`            | `ProductListView`     | `product_list`       | Lista todos os produtos.                |
| `products/create/`          | `ProductCreateView`   | `product_create`     | Exibe o formulário de registro de produto. |
| `products/<int:pk>/detail/` | `ProductDetailView`   | `product_detail`     | Mostra os detalhes de um produto.       |
| `products/<int:pk>/update/` | `ProductUpdateView`   | `product_update`     | Permite editar um produto existente.    |
| `products/<int:pk>/delete/` | `ProductDeleteView`   | `product_delete`     | Permite excluir um produto.             |

---

## 4. Forms (`forms.py`)

Os formulários são usados para criar e atualizar instâncias do modelo `Product`.

### `ProductForm`
- **Tipo:** `ModelForm`
- **Modelo Associado:** `Product`
- **Campos:** `title`, `category`, `brand`, `description`, `serial_number`, `cost_price`, `sale_price`, `quantity`.
- **Widgets Customizados:** (Inferido com base em outros apps)
  - Todos os campos de texto e seleção provavelmente usam a classe `form-control`.
  - `description`: `forms.Textarea` com a classe `form-control`.
  - `category`, `brand`: `forms.Select` com a classe `form-control`.
  - `cost_price`, `sale_price`, `quantity`: `forms.NumberInput` ou `forms.TextInput` com `type="number"` e a classe `form-control`.

---

## 5. Templates

- **`product_list.html`**: Página principal que exibe a lista de produtos em uma tabela. Inclui um formulário de busca e filtros (por título, número de série, categoria, marca), um botão para criar um "Novo Produto", botões de ação (detalhe, editar, excluir) para cada item, e o componente de paginação. Exibe também cartões com métricas gerais do estoque.
- **`product_create.html`**: (Inferido) Contém o formulário para adicionar um novo produto.
- **`product_detail.html`**: (Inferido) Exibe todas as informações de um único produto em modo de leitura.
- **`product_update.html`**: (Inferido) Contém o formulário para editar um produto existente.
- **`product_delete.html`**: (Inferido) Página de confirmação para a exclusão de um produto. Apresenta uma mensagem de alerta e botões para confirmar ou cancelar a ação.

---

## 6. Admin (`admin.py`)

Para uma melhor experiência de gerenciamento no Django Admin, uma configuração `ProductAdmin` pode ser criada e registrada.

### `ProductAdmin` (Sugestão)
- **`list_display`**: `title`, `category`, `brand`, `serial_number`, `quantity`, `cost_price`, `sale_price`, `created_at`, `updated_at`.
- **`search_fields`**: `title`, `serial_number`, `category__name`, `brand__name`.
- **`list_filter`**: `category`, `brand`, `created_at`, `updated_at`.
- **`autocomplete_fields`**: `category`, `brand`.
- **`fieldsets`**: Organização do formulário de edição em seções lógicas para melhor visualização.
  ```python
  fieldsets = (
      (None, {
          'fields': ('title', 'description', 'serial_number')
      }),
      ('Detalhes do Estoque', {
          'fields': ('category', 'brand', 'quantity', 'cost_price', 'sale_price')
      }),
      ('Informações de Auditoria', {
          'fields': ('created_at', 'updated_at'),
          'classes': ('collapse',), # Opcional: para recolher esta seção por padrão
      }),
  )
  readonly_fields = ('created_at', 'updated_at')
  ```