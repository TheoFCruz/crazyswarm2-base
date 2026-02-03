---
lang: "pt-BR"
---
# Anotações Crazyswarm2

## Desvio de colisões

Implementada no firmware

```yaml
all:
  firmware_parameters:
    colAv: 
      enabled: 1
```

ou

```python
swarm = Crazyswarm()
allcfs = swarm.allcfs
allcfs.setParam("colAv.enable", 1)
```

> **OBS**: Ainda não funciona na simulação (Discussion #357)

### Controle baixo nível

Quatro opções de tópico para comunicar direto com o crazyflie_server:

- /cfx/cmd_full_state: 

    Recebe posição, velocidade e aceleração desejadas (angular e linear). Teleop fornecido utiliza isso, mandando mensagens em intervalos de tempo constantes e realizando uma integração simples para definir qual a posição desejada a partir da velocidade. Ideal para seguir uma trajetória.

- /cfx/cmd_hover

    Recebe velocidades em x e y, altura e yaw desejados. As nodes de teleop por teclado utilizam esse tópico, a partir de vel_mux.py, que transforma mensagens Twist em Hover.
    
- /cfx/cmd_vel_legacy

    Controle baixo nível em roll, pitch, yaw e thrust.

- /cfx/cmd_position

    Controle direto pela posição desejada.

> **OBS**: Desses, apenas cmd_full_state funciona na simulação

Para usar em conjunto com os comandos alto nível é necessário chamar `notifySetpointsStop()`.

## Trajetória
