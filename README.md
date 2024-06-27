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



