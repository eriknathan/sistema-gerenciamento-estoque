# Documentação do App `categories`

Este documento detalha a estrutura e o funcionamento do aplicativo `categories` dentro do Sistema de Gerenciamento de Estoque (SGE). O objetivo deste app é gerenciar as categorias dos produtos cadastrados no sistema.

## 1. Model (`models.py`)

O coração do app é o modelo `Category`, que representa uma categoria de produto.

### `Category`

| Campo         | Tipo              | Descrição                                           | Opções                                   |
| :------------ | :---------------- | :-------------------------------------------------- | :--------------------------------------- |
| `name`        | `CharField(255)`  | Nome da categoria.                                  | Obrigatório, `verbose_name="Nome"`       |
| `description` | `TextField`       | Descrição ou observações sobre a categoria.         | Opcional, `verbose_name="Descrição"`     |
| `is_active`   | `BooleanField`    | Indica se a categoria está ativa no sistema.        | Padrão: `True`, `verbose_name="Ativo"`     |
| `created_at`  | `DateTimeField`   | Data e hora de criação do registro.                 | `auto_now_add=True`                      |
| `updated_at`  | `DateTimeField`   | Data e hora da última atualização do registro.      | `auto_now=True`                          |

**Meta Opções:**
- `verbose_name`: 'Categoria'
- `verbose_name_plural`: 'Categorias'
- `ordering`: ['name'] (As listagens são ordenadas pelo nome da categoria por padrão).

**Relações:**
- **Produto (`Product`):** Uma categoria pode estar associada a vários produtos. A relação é definida no modelo `Product` com `on_delete=models.PROTECT`, o que impede que uma categoria seja excluída se houver produtos associados a ela.

---

## 2. Views (`views.py`)

As views são baseadas em classes (Class-Based Views) do Django, facilitando a implementação das operações de CRUD (Create, Read, Update, Delete).

### `CategoryListView`
- **Tipo:** `ListView`
- **Função:** Lista todas as categorias cadastradas, com paginação de 10 itens por página.
- **Template:** `category_list.html`
- **Contexto:** A lista de categorias é injetada no template com o nome `categories`.
- **Funcionalidade Extra:** Suporta busca por nome através de um parâmetro GET `name`. A busca filtra categorias cujo nome contém o texto fornecido (case-insensitive).

### `CategoryCreateView`
- **Tipo:** `CreateView`
- **Função:** Exibe um formulário para criar uma nova categoria.
- **Template:** `category_create.html`
- **Formulário:** `CategoryForm`
- **Sucesso:** Após a criação, redireciona para a URL `category_list`.

### `CategoryDetailView`
- **Tipo:** `DetailView`
- **Função:** Exibe os detalhes de uma categoria específica.
- **Template:** `category_detail.html`
- **Contexto:** O objeto da categoria é injetado no template com o nome `category`.

### `CategoryUpdateView`
- **Tipo:** `UpdateView`
- **Função:** Exibe um formulário preenchido com os dados de uma categoria existente para edição.
- **Template:** `category_update.html`
- **Formulário:** `CategoryForm`
- **Sucesso:** Após a atualização, redireciona para a URL `category_list`.

### `CategoryDeleteView`
- **Tipo:** `DeleteView`
- **Função:** Exibe uma página de confirmação antes de excluir uma categoria.
- **Template:** `category_delete.html`
- **Sucesso:** Após a exclusão, redireciona para a URL `category_list`.

---

## 3. URLs (`urls.py`)

As URLs mapeiam os caminhos da web para as views correspondentes.

| URL Path                    | View                    | Nome da URL (`name`)  | Descrição                                 |
| :-------------------------- | :---------------------- | :-------------------- | :---------------------------------------- |
| `categories/list/`          | `CategoryListView`      | `category_list`       | Lista todas as categorias.                |
| `categories/create/`        | `CategoryCreateView`    | `category_create`     | Exibe o formulário de criação de categoria. |
| `categories/<int:pk>/detail/` | `CategoryDetailView`    | `category_detail`     | Mostra os detalhes de uma categoria.      |
| `categories/<int:pk>/update/` | `CategoryUpdateView`    | `category_update`     | Permite editar uma categoria existente.   |
| `categories/<int:pk>/delete/` | `CategoryDeleteView`    | `category_delete`     | Permite excluir uma categoria.            |

---

## 4. Forms (`forms.py`)

Os formulários são usados para criar e atualizar instâncias do modelo `Category`.

### `CategoryForm`
- **Tipo:** `ModelForm`
- **Modelo Associado:** `Category`
- **Campos:** `name`, `description`, `is_active`.
- **Widgets Customizados:**
  - `name`: `forms.TextInput` com a classe CSS `form-control`.
  - `description`: `forms.Textarea` com a classe `form-control` e 3 linhas de altura.
  - `is_active`: `forms.CheckboxInput` estilizado como um "switch" com as classes `form-check-input` e `role="switch"`.
- **Labels:**
  - `name`: 'Nome'
  - `description`: 'Descrição'

---

## 5. Templates

Os templates são responsáveis pela interface do usuário.

- **`category_list.html`**: Página principal que exibe a lista de categorias em uma tabela. Inclui um formulário de busca, um botão para criar uma nova categoria e botões de ação (detalhe, editar, excluir) para cada item. Também inclui o componente de paginação.
- **`category_create.html`**: (Inferido) Contém o formulário para adicionar uma nova categoria.
- **`category_update.html`**: (Inferido) Contém o formulário para editar uma categoria existente.
- **`category_detail.html`**: (Inferido) Exibe as informações de uma única categoria em modo de leitura.
- **`category_delete.html`**: (Inferido) Página de confirmação para a exclusão de uma categoria. Apresenta uma mensagem de alerta e botões para confirmar ou cancelar a ação.

---

## 6. Admin (`admin.py`)

A integração com o Django Admin permite o gerenciamento das categorias diretamente pela interface administrativa.

### `CategoryAdmin`
- **`list_display`**: Define as colunas exibidas na listagem de categorias: `name`, `description`, `is_active`, `created_at`, `updated_at`.
- **`search_fields`**: Adiciona um campo de busca que filtra as categorias pelo campo `name`.

O modelo `Category` é registrado no admin site junto com a classe `CategoryAdmin` para aplicar essas customizações.