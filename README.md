Repositório criado para o projeto final da disciplina de Sistemas Distribuidos

# Price Tracker

Este trabalho consiste em um BOT para telegram que supervisionará anúncios de sites de e-commerce ([Kabum](https://www.kabum.com.br/)), onde será possível enviar o link de um anúncio, e o bot fará o monitoramento do preço do produto.

O monitoramento será feito através de Web Scraping ([Selenium]([https://www.selenium.dev/documentation/](https://www.selenium.dev/))) através de um sistema publish-subscribe ([RabbitMQ](https://www.rabbitmq.com/)), em que a cada um certo tempo o preço será verificado e caso haja mudanças, o bot enviará as informações do produto.

Também será possível verificar o histórico de preços do produto durante o tempo monitorado, retornando um gráfico dos preços anteriores.
