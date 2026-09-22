# delvecchio_rl26

Ambiente di sviluppo per Robotics Lab 2026 — Classwork 0.

## Prerequisiti

* Ambiente Linux: Ubuntu 22.04, WSL2 oppure macchina virtuale.
* Git e Docker installati.
* Servizio Docker avviato e utente autorizzato a eseguire i comandi Docker.
* Comando `xhost` disponibile per gli script di avvio e collegamento.

I comandi seguenti assumono che il progetto si trovi in `~/Scrivania/delvecchio_rl26`.

## Preparazione

Dalla cartella principale del progetto, rendere eseguibili gli script:

```bash
cd ~/Scrivania/delvecchio_rl26
chmod +x docker_scripts/*.sh
```

## Build dell’immagine

Eseguire la build dalla cartella contenente il Dockerfile:

```bash
cd docker_scripts
./docker_build_image.sh delvecchio_rl26_img
cd ..
```

## Avvio del container

Dalla cartella principale del progetto:

```bash
./docker_scripts/docker_run_container.sh
```

Nel wizard selezionare:

* Immagine: `delvecchio_rl26_img`
* Nome del container: `delvecchio_rl26_cont`
* Cartella: `Scrivania/delvecchio_rl26/src`

Lo script aggiunge automaticamente `/home/$USER/` al percorso della cartella. Non inserire `~/` o un percorso assoluto nel wizard.

La cartella `src` del computer viene montata in `/home/user/ros2_ws/src` nel container.

## Verifica di ROS 2

Dentro il container:

```bash
echo $ROS_DISTRO
ros2 pkg list
```

Il primo comando deve stampare `humble`; il secondo deve elencare i pacchetti ROS 2 disponibili.

## Collegamento da un altro terminale

Lasciare aperto il terminale iniziale. In un secondo terminale del computer:

```bash
cd ~/Scrivania/delvecchio_rl26
./docker_scripts/docker_connect.sh
```

Selezionare `delvecchio_rl26_cont` per aprire un’altra shell nel container.

## Verifica della persistenza

Nella seconda shell del container, creare un file nella cartella condivisa e uscire:

```bash
touch /home/user/ros2_ws/src/test_persistence.txt
exit
```

Nel primo terminale del container, eseguire:

```bash
exit
```

Il container viene arrestato e rimosso automaticamente grazie all’opzione `--rm` dello script di avvio.

Sul computer, verificare che il file sia ancora presente:

```bash
ls -l ~/Scrivania/delvecchio_rl26/src/test_persistence.txt
```

La presenza del file dopo la rimozione del container conferma la persistenza dei dati nella cartella condivisa.

## Verifiche completate

* Avvio del container.
* Distribuzione ROS 2: `humble`.
* Elenco dei pacchetti ROS 2 disponibile.
* Collegamento da un secondo terminale.
* File di prova presente sul computer dopo la rimozione del container.
