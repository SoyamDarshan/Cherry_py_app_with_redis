import os
import cherrypy
from jinja2 import Environment, FileSystemLoader
import redis_connection
import read_csv_file


CURR_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(CURR_DIR), trim_blocks=True)


class Index(object):
    @cherrypy.expose()
    def index(self):
        template = env.get_template('top_10_values.html')
        table_data = redis_connection.get_top_10_stocks()
        # print(table_data)
        return template.render(title='Stock Data',
                               description="Top 10 stock",
                               table_data=table_data)

    @cherrypy.expose()
    def search(self, search_value):
        try:
            template = env.get_template('search_result.html')
            table_data = redis_connection.get_stock_value(search_value)
            return template.render(title='Stock Data',
                                   description="search value",
                                   table_data=table_data,
                                   )
        except:
            template = env.get_template('search_result_not_found.html')
            return template.render(title='Not Found')


if __name__ == '__main__':
    conf = {"/static/css": {"tools.staticdir.on": True,
                            "tools.staticdir.dir": os.path.abspath("./static/css/"), },
            'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
        '/': {
        'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    }
    # print(conf)
    cherrypy.quickstart(Index(), '/', config=conf)
