# Estrutura do Dataset de Gestos Manuais

Este ambiente utiliza o pipeline **MediaPipe Gesture Recognizer**, que é estritamente baseado no rastreamento de pontos anatômicos da mão (**Hand Landmarks**).

### Requisitos Anatômicos Obrigatórios:
- **Apenas Mãos:** Todas as imagens devem conter pelo menos uma **mão humana claramente visível**.
- Imagens que contenham apenas rostos, corpos sem mãos ou fundos vazios serão automaticamente ignoradas pelo extrator do Google durante a extração de features.

### Labels 100% Dinâmicas (Zero Presets):
Não há classes pré-definidas no código. As labels são criadas dinamicamente com base no nome de cada subpasta que você criar dentro de `dataset/`.

### Exemplo de Estrutura:
```text
dataset/
├── none/                    <-- Classe de controle / mão em repouso (altamente recomendada)
│   ├── foto_001.jpg
│   └── foto_002.jpg
├── gesto_personalizado_a/   <-- Nome do seu gesto manual customizado
│   ├── foto_001.jpg
│   └── foto_002.jpg
└── gesto_personalizado_b/   <-- Outro gesto manual customizado
    ├── foto_001.jpg
    └── foto_002.jpg
```

> **Dicas de Captura:**
> - A classe `none` serve como estado neutro ou ausência de gesto ativo.
> - Formatos recomendados: `.jpg`, `.jpeg` ou `.png`.
> - Recomenda-se de 30 a 100 imagens por classe com variações de ângulos, iluminação e distância para melhor robustez.
