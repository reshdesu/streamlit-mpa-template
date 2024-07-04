"Docker builder python code for streamlit_mpa_template project"
import docker
from loguru import logger
import socket

logger.enable(__package__)


class BuildHelper:
    def __init__(self):
        self.client = docker.from_env()

    def prune_dangling_images(self):
        self.client.images.prune(filters={"dangling": True})

    def build_image(self):
        """
        Build image for the project
        Info can be found:
        https://docs.streamlit.io/deploy/tutorials/docker
        https://docker-py.readthedocs.io/en/stable/containers.html
        """
        # check if the image is already present
        # this will happen on each new rebuild
        docker_images = self.client.images.list(name="streamlit_mpa_template")
        # remove the image is it exists
        if len(docker_images) > 0:
            for docker_image in docker_images:
                logger.info(f"Trying to remove image {docker_image}")
                self.client.images.remove(image=docker_image.id)
                # self.client.images.prune(filters={"dangling": True})
                logger.info(f"Removed {docker_image}")
        # build a new image
        logger.info("Building new image")
        # we had to move the docker file outside the build directory as it was unable to copy the src folder
        # [ERROR] docker.errors.BuildError: ADD failed: forbidden path outside the build context: ../src ()
        # have to padd path of root folder so that we can allow Dockerfile to be found
        self.client.images.build(path=".", tag="streamlit_mpa_template")
        # prune dangling images after the rebuild
        self.client.images.prune(filters={"dangling": True})
        logger.info("Finished building image!")

    def run_container(self):
        """
        Run a container on the built image for the project
        Info can be found:
        https://docs.streamlit.io/deploy/tutorials/docker
        https://docker-py.readthedocs.io/en/stable/containers.html
        """
        # check if the container is already present
        # this will happen on each new rebuild
        docker_containers = self.client.containers.list(all=True)
        if len(docker_containers) > 0:
            for docker_container in docker_containers:
                if docker_container.name == "streamlit_mpa_template_container":
                    logger.info(f"Cleaning up {docker_container.name}")
                    docker_container.stop()
                    docker_container.remove()
                    logger.info(f"Cleaned up {docker_container.name}!")

        # rebuild the image
        self.build_image()
        # running streamlit_mpa_template container on the image
        port = 8000
        self.client.containers.run(
            image="streamlit_mpa_template",
            hostname="0.0.0.0",
            name="streamlit_mpa_template_container",
            ports={port: port},
            detach=True,
        )
        logger.info(
            f"""Started streamlit_mpa_template_container on http://{socket.gethostname().lower()}:{port}/"""
        )
