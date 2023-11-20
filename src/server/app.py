import uvicorn
from fastapi import FastAPI

from config_parsing import ConfigParser, EnvConfigParser
from services.extraction import Extractor
from services.extraction.html_extraction import HTMLExtractor

from routing import Routes


app = FastAPI()

config_parser: ConfigParser = EnvConfigParser()
extractor: Extractor = HTMLExtractor()
routes: Routes = Routes(extractor)
app.include_router(routes.router)


if __name__ == '__main__':
    uvicorn.run(app=app, host=config_parser.parse_host(), port=config_parser.parse_port())
