# DICOM-to-PNG
# Conversor DICOM para JPG

Ferramenta desenvolvida em **Python** para conversão de arquivos de imagem médica no formato **DICOM (.dcm)** para imagens **JPG (.jpg)**.

O projeto permite converter um único arquivo DICOM ou realizar a conversão em lote de todos os arquivos `.dcm` presentes em uma pasta.

Objetivo

O projeto foi desenvolvido com o objetivo de facilitar a conversão de imagens médicas armazenadas no formato DICOM para um formato de imagem convencional, permitindo sua utilização em aplicações que não trabalham diretamente com arquivos DICOM.

A ferramenta foi desenvolvida com foco em:

- Conversão de arquivos DICOM para JPG;
- Processamento de imagens em tons de cinza e RGB;
- Conversão de múltiplos arquivos em lote;
- Ajuste da faixa de valores de imagens com mais de 8 bits;
- Utilização por linha de comando;
- Utilização através de seleção de pastas no Windows;
- Geração de um executável `.exe`.

---

Sobre o formato DICOM

**DICOM (Digital Imaging and Communications in Medicine)** é um padrão utilizado para armazenamento e comunicação de imagens médicas e informações relacionadas aos exames.

Um arquivo DICOM pode armazenar, além dos dados de imagem, diversas informações associadas ao exame.

Neste projeto, o foco está na **leitura dos dados de pixel e conversão da imagem para JPG**.

Este projeto tem finalidade técnica e educacional. A imagem convertida não deve ser utilizada como substituição de softwares médicos destinados à visualização ou diagnóstico de exames.

---

Funcionamento

O processo de conversão segue, de forma simplificada, o fluxo:

```text
Arquivo DICOM (.dcm)
        │
        ▼
   pydicom.dcmread()
        │
        ▼
  Dados de pixel
        │
        ▼
Identificação da imagem
 (RGB / tons de cinza)
        │
        ▼
Tratamento de múltiplos frames
        │
        ▼
Normalização dos valores
 quando necessário
        │
        ▼
Conversão para uint8
        │
        ▼
      Pillow
        │
        ▼
Imagem JPG (.jpg)
```

---

Tecnologias utilizadas

- **Python**
- **pydicom** — leitura e processamento de arquivos DICOM;
- **NumPy** — manipulação da matriz de pixels e normalização dos valores;
- **Pillow (PIL)** — criação e salvamento da imagem;
- **argparse** — processamento dos argumentos da linha de comando;
- **Tkinter** — seleção de pastas através de uma interface gráfica simples;
- **PyInstaller** — geração do executável para Windows.

---

Funcionalidades

### Conversão de um arquivo

É possível informar um único arquivo DICOM e definir o caminho do arquivo JPG de saída.

### Conversão em lote

Ao informar uma pasta como entrada, o programa identifica automaticamente os arquivos com extensão `.dcm` e converte cada um deles.

Exemplo:

```text
Pasta de entrada
│
├── exame01.dcm
├── exame02.dcm
├── exame03.dcm
└── exame04.dcm
```

Resultado:

```text
Pasta de saída
│
├── exame01.jpg
├── exame02.jpg
├── exame03.jpg
└── exame04.jpg
```

### Interface de seleção de pastas

Quando o programa é executado sem argumentos, são abertas janelas para selecionar:

1. A pasta contendo os arquivos DICOM;
2. A pasta onde os JPGs serão salvos.

Isso permite utilizar a ferramenta sem precisar informar os caminhos manualmente pelo terminal.

---

Processamento das imagens

O programa verifica a quantidade de amostras por pixel (`SamplesPerPixel`) para identificar imagens RGB.

### Imagens em tons de cinza

Para imagens que não são RGB, o programa trabalha com a matriz de pixels e realiza uma normalização dos valores.

Quando necessário, os valores são convertidos para uma faixa de **0 a 255**, permitindo a representação da imagem em 8 bits.

### Imagens com mais de 8 bits

Arquivos DICOM podem armazenar imagens utilizando uma profundidade maior que 8 bits.

Quando `BitsAllocated` é superior a 8, o programa calcula os valores mínimo e máximo encontrados na imagem e realiza uma normalização:

```text
valor original
      │
      ▼
mínimo → máximo
      │
      ▼
0 → 255
```

Posteriormente, os valores são convertidos para `uint8`.

### Imagens RGB

Quando o arquivo possui `SamplesPerPixel = 3`, a imagem é tratada como RGB:

```python
Image.fromarray(image_data, 'RGB')
```

---

Múltiplos frames

O programa também verifica arquivos DICOM que possuem múltiplos frames.

Atualmente, quando um arquivo contém múltiplos frames, **somente o primeiro frame é convertido**.

O programa apresenta um aviso no terminal:

```text
Aviso: arquivo.dcm contém múltiplos frames.
Apenas o primeiro será convertido.
```

Essa decisão evita a tentativa de salvar vários frames em uma única imagem JPG.

---

Como executar

### Pré-requisitos

É necessário possuir o Python instalado.

As dependências podem ser instaladas utilizando:

pip install pydicom numpy Pillow


Ou 

pip install -r requirements.txt



Modo gráfico

Executando o programa sem argumentos:

```bash
python main.py
```

O programa solicitará a seleção da pasta de origem:

```text
1. Selecione a pasta que contém as imagens DICOM originais...
```

Em seguida, será solicitada a pasta de destino:

```text
2. Selecione a pasta onde deseja salvar os JPGs...
```

Após a seleção, os arquivos `.dcm` encontrados na pasta serão processados automaticamente.

---

## ⌨️ Modo linha de comando

O programa também pode ser executado pelo terminal.

### Converter uma pasta

```bash
python main.py "C:\caminho\entrada" "C:\caminho\saida"
```

O programa irá procurar arquivos `.dcm` na pasta de entrada e salvar os JPGs na pasta de saída.

### Converter um único arquivo

```bash
python main.py "C:\caminho\exame.dcm" "C:\caminho\exame.jpg"
```

Também é possível informar uma pasta como destino:

```bash
python main.py "C:\caminho\exame.dcm"   "C:\caminho\saida"
```

Nesse caso, o nome do arquivo JPG será baseado no nome original do DICOM.

---

---

Geração do executável

O projeto pode ser empacotado como um executável para Windows utilizando o **PyInstaller**.

Exemplo:

```bash
pyinstaller --onefile main.py
```

O executável será disponibilizado no diretório:

DICOM-to-JPG.exe
```

---

Tratamento de erros

O programa possui tratamento de exceções durante:

- Leitura do arquivo DICOM;
- Processamento da matriz de pixels;
- Conversão da imagem;
- Salvamento do arquivo de saída;
- Seleção das pastas.

Quando ocorre um erro, uma mensagem é apresentada no terminal.

Exemplo:

```text
Erro ao ler arquivo.dcm: ...
```

---

Limitações atuais

Atualmente, o projeto possui algumas limitações conhecidas:

- Apenas arquivos com extensão `.dcm` são processados durante a conversão de pastas;
- Em arquivos com múltiplos frames, somente o primeiro frame é convertido;
- A normalização dos valores de pixel é baseada nos valores mínimo e máximo encontrados na imagem;
- O projeto atualmente gera arquivos **JPG**, não PNG;
- O projeto não possui uma interface gráfica completa; a seleção de pastas é realizada através do Tkinter;
- O projeto não possui atualmente uma suíte de testes automatizados.

---

Próximas melhorias

Possíveis melhorias para versões futuras:

- [ ] Adicionar suporte à conversão para PNG;
- [ ] Permitir escolha do formato de saída;
- [ ] Melhorar o tratamento de diferentes tipos de DICOM;
- [ ] Suporte adequado para múltiplos frames;
- [ ] Criar uma interface gráfica completa;
- [ ] Adicionar barra de progresso;
- [ ] Adicionar logs de conversão;
- [ ] Implementar testes automatizados;
- [ ] Melhorar o tratamento de diferentes profundidades de imagem;
- [ ] Adicionar informações sobre quantidade de arquivos processados;
- [ ] Criar versão distribuível do executável.

---

Conceitos trabalhados

O desenvolvimento deste projeto envolve conceitos de:

- Programação em Python;
- Manipulação de arquivos e diretórios;
- Processamento de imagens;
- Manipulação de matrizes;
- Conversão de tipos numéricos;
- Normalização de dados;
- Processamento de imagens médicas;
- Tratamento de exceções;
- Argumentos de linha de comando;
- Interface básica com Tkinter;
- Empacotamento de aplicações com PyInstaller.

---

Autores

**Luiz Weber**  
Estudante de Engenharia Eletrônica — UTFPR

Projeto desenvolvido com finalidade de aprendizado, desenvolvimento técnico e construção de portfólio.
