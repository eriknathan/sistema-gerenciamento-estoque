# Documentação do App `brands`

Este documento detalha a estrutura e o funcionamento do aplicativo `brands` dentro do Sistema de Gerenciamento de Estoque (SGE). O objetivo deste app é gerenciar as marcas dos produtos cadastrados no sistema.

## 1. Model (`models.py`)

O coração do app é o modelo `Brand`, que representa uma marca de produto.

### `Brand`

| Campo         | Tipo              | Descrição                                         | Opções                               |
| :------------ | :---------------- | :------------------------------------------------ | :----------------------------------- |
| `name`        | `CharField(255)`  | Nome da marca.                                    | Obrigatório, `verbose_name="Nome"`   |
| `description` | `TextField`       | Descrição ou observações sobre a marca.           | Opcional, `verbose_name="Descrição"` |
| `is_active`   | `BooleanField`    | Indica se a marca está ativa no sistema.          | Padrão: `True`, `verbose_name="Ativo"` |
| `created_at`  | `DateTimeField`   | Data e hora de criação do registro.               | `auto_now_add=True`                  |
| `updated_at`  | `DateTimeField`   | Data e hora da última atualização do registro.    | `auto_now=True`                      |

**Meta Opções:**
- `verbose_name`: 'Marca'
- `verbose_name_plural`: 'Marcas'
- `ordering`: ['name'] (As listagens são ordenadas pelo nome da marca por padrão).

**Relações:**
- **Produto (`Product`):** Uma marca pode estar associada a vários produtos. A relação é definida no modelo `Product` com `on_delete=models.PROTECT`, o que impede que uma marca seja excluída se houver produtos associados a ela.

---

## 2. Views (`views.py`)

As views são baseadas em classes (Class-Based Views) do Django, facilitando a implementação das operações de CRUD (Create, Read, Update, Delete).

### `BrandListView`
- **Tipo:** `ListView`
- **Função:** Lista todas as marcas cadastradas, com paginação de 10 itens por página.
- **Template:** `brand_list.html`
- **Contexto:** A lista de marcas é injetada no template com o nome `brands`.
- **Funcionalidade Extra:** Suporta busca por nome através de um parâmetro GET `name`. A busca filtra marcas cujo nome contém o texto fornecido (case-insensitive).

### `BrandCreateView`
- **Tipo:** `CreateView`
- **Função:** Exibe um formulário para criar uma nova marca.
- **Template:** `brand_create.html`
- **Formulário:** `BrandForm`
- **Sucesso:** Após a criação, redireciona para a URL `brand_list`.

### `BrandDetailView`
- **Tipo:** `DetailView`
- **Função:** Exibe os detalhes de uma marca específica.
- **Template:** `brand_detail.html`
- **Contexto:** O objeto da marca é injetado no template com o nome `brand`.

### `BrandUpdateView`
- **Tipo:** `UpdateView`
- **Função:** Exibe um formulário preenchido com os dados de uma marca existente para edição.
- **Template:** `brand_update.html`
- **Formulário:** `BrandForm`
- **Sucesso:** Após a atualização, redireciona para a URL `brand_list`.

### `BrandDeleteView`
- **Tipo:** `DeleteView`
- **Função:** Exibe uma página de confirmação antes de excluir uma marca.
- **Template:** `brand_delete.html`
- **Sucesso:** Após a exclusão, redireciona para a URL `brand_list`.

---

## 3. URLs (`urls.py`)

As URLs mapeiam os caminhos da web para as views correspondentes.

| URL Path                  | View                  | Nome da URL (`name`) | Descrição                               |
| :------------------------ | :-------------------- | :------------------- | :-------------------------------------- |
| `brands/list/`            | `BrandListView`       | `brand_list`         | Lista todas as marcas.                  |
| `brands/create/`          | `BrandCreateView`     | `brand_create`       | Exibe o formulário de criação de marca. |
| `brands/<int:pk>/detail/` | `BrandDetailView`     | `brand_detail`       | Mostra os detalhes de uma marca.        |
| `brands/<int:pk>/update/` | `BrandUpdateView`     | `brand_update`       | Permite editar uma marca existente.     |
| `brands/<int:pk>/delete/` | `BrandDeleteView`     | `brand_delete`       | Permite excluir uma marca.              |

---

## 4. Forms (`forms.py`)

Os formulários são usados para criar e atualizar instâncias do modelo `Brand`.

### `BrandForm`
- **Tipo:** `ModelForm`
- **Modelo Associado:** `Brand`
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

- **`brand_list.html`**: Página principal que exibe a lista de marcas em uma tabela. Inclui um formulário de busca, um botão para criar uma nova marca e botões de ação (detalhe, editar, excluir) para cada item. Também inclui o componente de paginação.
- **`brand_create.html`**: (Não fornecido, mas inferido) Contém o formulário para adicionar uma nova marca.
- **`brand_update.html`**: (Não fornecido, mas inferido) Contém o formulário para editar uma marca existente.
- **`brand_detail.html`**: (Não fornecido, mas inferido) Exibe as informações de uma única marca em modo de leitura.
- **`brand_delete.html`**: Página de confirmação para a exclusão de uma marca. Apresenta uma mensagem de alerta e botões para confirmar ou cancelar a ação.

---

## 6. Admin (`admin.py`)

A integração com o Django Admin permite o gerenciamento das marcas diretamente pela interface administrativa.

### `BrandAdmin`
- **`list_display`**: Define as colunas exibidas na listagem de marcas: `name`, `description`, `is_active`, `created_at`, `updated_at`.
- **`search_fields`**: Adiciona um campo de busca que filtra as marcas pelo campo `name`.

O modelo `Brand` é registrado no admin site junto com a classe `BrandAdmin` para aplicar essas customizações.

