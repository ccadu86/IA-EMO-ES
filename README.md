# Projeto IA - Reconhecimento de emoções

<aside>
💡 A ideia principal do projeto é utilizar uma API da Google (Cloud Vision), para extrair emoções do usuário, pela webcam.

</aside>

Na configuração proposta, os equipamentos principais são: um botão, um monitor, uma Raspberry Pi e uma webcam. O procedimento se inicia com o usuário posicionando seu rosto diante da webcam para que seja exibido na tela do monitor. Em seguida, o botão é pressionado para acionar o processo de captura de imagem. Automaticamente, a foto é tirada e os dados faciais são enviados para uma API por meio de uma requisição. Após um curto período, a foto capturada é apresentada na tela juntamente com um retângulo que delimita o rosto do usuário, acompanhado de uma legenda que descreve a emoção identificada.


## `Esquema visual - Brainstorming:`

![Brainstorming](https://github.com/ccadu86/IA-EMO-ES/assets/134337212/65148cd1-6bc1-43fa-b73c-59895b9457a3)

## `GCP:`

- Cloud Vision;
- Credenciais.

## `RASP:`

- Request → API GCP;
- JSON → Chaves.

## `Estética visual:`

Planejamento de uma estética visual visando o relacionamento entre o usuário, o monitor, e o botão que será usado para iniciar o processo de captura.

## **`Equipamentos:`**

- Raspberrry Pi 4;
- Monitor;
- Webcam.

## `Software:`

- Instalação do VSCODE;
- Instalação da Rasp OS Debian;
- Instalação do GIT.

## `Hardware:`

- Botão → Resistor → Pull-Down.

## Raspberry

→ Link para o site oficial: [Raspberry Pi](https://www.raspberrypi.com/)

### O que é a Raspberry?

![Raspberry](https://github.com/ccadu86/IA-EMO-ES/assets/134337212/b9b85bec-d499-4b02-9375-d6b8365db440)

O Raspberry Pi (RPi) é um microcomputador de placa única projetado pela Raspberry Pi Foundation, lançado inicialmente em 2012 com o modelo Raspberry Pi 1 Model B. Ele é uma alternativa acessível e compacta aos computadores tradicionais, contendo todos os componentes essenciais em uma única placa.

Equipado com processador, memória RAM, placa de vídeo integrada e diversos conectores (como USB, HDMI, áudio e GPIO), o Raspberry Pi suporta sistemas operacionais baseados em Linux e pode ser utilizado para uma variedade de finalidades. Desde atividades educacionais em programação e eletrônica até projetos de automação residencial, servidores de mídia, IoT e prototipagem.

### Procedimento para utilização da Raspberry

**→ Download da imagem da Raspberry no cartão SD**

![Download Rasp](https://github.com/ccadu86/IA-EMO-ES/assets/134337212/43c0610e-1f53-4f49-a8e4-995e1e0473f7)

**→ Configurar Raspberry Pi Imager**

![Config rasp](https://github.com/ccadu86/IA-EMO-ES/assets/134337212/29791fca-ad97-4d61-bffe-ee43250a3af7)

- **Raspberry Pi Device:** Raspberry Pi 4;
- **Operating System:** Raspberry Pi OS (64-bit);
- **Storage:** Generic- SD/MMC/MS PRO USB Device-31.9GB.

**→ NEXT**

![Customisation Rasp](https://github.com/ccadu86/IA-EMO-ES/assets/134337212/8344d348-7e68-4a7c-832f-895cf0a83e82)

**→ EDIT SETTINGS**

→ GENERAL:

![Settings rasp](https://github.com/ccadu86/IA-EMO-ES/assets/134337212/a07bbbdd-b534-4ff2-beec-7f1f6c07fe0d)

Configurações:

- **Set hostname:** projetoIA;
- **Username:** instrutor;
- **Set locale settings**
- **Time zone:** America/Sao_Paulo;
- **Keyboard layout:** pt.

→ SAVE

→ SERVICES:

![Services rasp](https://github.com/ccadu86/IA-EMO-ES/assets/134337212/2c7861d8-8ddd-413a-b28b-e59ce0b62115)

Enable SSH ✅

SSH - É um protocolo de comunicação remoto via terminal, pelo terminal conseguimos acessar a RASP e realizar configurações.

→ SAVE

![SAVE RASP](https://github.com/ccadu86/IA-EMO-ES/assets/134337212/8e28c164-d4c5-4573-8ebd-8418f36f6557)

→ Clicar no botão “YES” para a criação da imagem no cartão SD.

## Python

→ Link para o site oficial: (https://www.python.org/)

### Preparação do ambiente - Python:

→ Instalação e Configuração do VScode

Obs: A instalação do VScode foi realizada somente para o desenvolvimento do projeto. Após a aprovação da interface, a utilização do python passou a ser utilizada pelo terminal, para melhorar a otimização.

*Antes da instalação do VScode, a própria Rasp dá uma opção para a atualização dos sistema operacional.

→ No terminal:

```python
pip install code
```

```python
code
```

→ No VScode, realizar a instalação e ativação do python (extensões): 

![Extensoes Py](https://github.com/ccadu86/IA-EMO-ES/assets/134337212/6926ddcb-4f7e-4faf-9f1c-7b189e5482e0)

---

### `Configuração do ambiente sem o VScode`

→ Preparação do ambiente pelo terminal:

- Atualização dos pacotes da RASP

```jsx
sudo apt-get update
sudo apt-get upgrade
```

- Criação de pasta para o projeto

```jsx
MKDIR ProjetoIA
```

- Clonar o repositório do git

```jsx
git clone https://github.com/ccadu86/IA-EMO-ES.git
```

- Criação de ambiente virtual

```jsx
python -m venv venv
```

- Ativar ambiente virtual

```jsx
source venv/bin/activate
```

- Instalações das bibliotecas

```jsx
pip install opencv-python
pip install --upgrade google-cloud-vision
pip install RPi-GPIO
```

- Start aplicação

```jsx
python main.py
```

