# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codex',
 'codex.librarian',
 'codex.librarian.covers',
 'codex.librarian.db',
 'codex.librarian.janitor',
 'codex.librarian.search',
 'codex.librarian.watchdog',
 'codex.logger',
 'codex.migrations',
 'codex.notifier',
 'codex.search',
 'codex.serializers',
 'codex.settings',
 'codex.urls',
 'codex.urls.api',
 'codex.urls.opds',
 'codex.views',
 'codex.views.admin',
 'codex.views.browser',
 'codex.views.browser.filters',
 'codex.views.opds_v1',
 'codex.views.reader',
 'tests']

package_data = \
{'': ['*'],
 'codex': ['img/missing-cover.webp',
           'static_root/*',
           'static_root/admin/css/*',
           'static_root/admin/js/*',
           'static_root/assets/*',
           'static_root/img/*',
           'static_root/js/*',
           'static_root/pwa/*',
           'static_root/rest_framework/css/*',
           'static_root/rest_framework/docs/css/*',
           'static_root/rest_framework/docs/img/*',
           'static_root/rest_framework/docs/js/*',
           'static_root/rest_framework/fonts/*',
           'static_root/rest_framework/img/*',
           'static_root/rest_framework/js/*',
           'templates/*',
           'templates/opds/*',
           'templates/pwa/*',
           'templates/search/indexes/codex/*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'ansicolors>=1.1,<2.0',
 'comicbox>=0.6.4,<0.7.0',
 'django-cors-headers>=3.2,<4.0',
 'django-haystack>=3.2.1,<4.0.0',
 'django-rest-registration>=0.7.2,<0.8.0',
 'django-vite>=2.0.2,<3.0.0',
 'django>=4.1,<5.0',
 'djangorestframework-camel-case>=1.3.0,<2.0.0',
 'djangorestframework>=3.11,<4.0',
 'drf-spectacular>=0.25.0,<0.26.0',
 'filelock>=3.4.2,<4.0.0',
 'filetype>=1.0.12,<2.0.0',
 'fnvhash>=0.1,<0.2',
 'humanfriendly>=10.0,<11.0',
 'humanize>=4.0.0,<5.0.0',
 'hypercorn[h3]>=0.14.1,<0.15.0',
 'pdf2image>=1.16.0,<2.0.0',
 'pdfrw>=0.4,<0.5',
 'pycountry>=22.1,<23.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.24,<3.0',
 'tzlocal>=4.1,<5.0',
 'watchdog>=2.0,<3.0',
 'websocket_client>=1.2,<2.0',
 'whitenoise[brotli]>=6.0,<7.0',
 'whoosh>=2.7.4,<3.0.0']

entry_points = \
{'console_scripts': ['codex = codex.run:main']}

setup_kwargs = {
    'name': 'codex',
    'version': '1.1.4a0',
    'description': 'A comic archive web server.',
    'long_description': '# Codex\n\nA comic archive browser and reader.\n\n<img src="codex/static_src/img/logo.svg" style="\nheight: 128px;\nwidth: 128px;\nborder-radius: 128px;\n" />\n\n## <a name="features">✨ Features</a>\n\n- Codex is a web server.\n- Full text search of metadata and bookmarks.\n- Filter and sort on all comic metadata and unread status per user.\n- Browse a tree of publishers, imprints, series, volumes, or your own folder\n  hierarchy.\n- Read comics in a variety of aspect ratios that fit your screen.\n- Per user bookmarking. Per browser bookmarks even before you make an account.\n- Watches the filesystem and automatically imports new or changed comics.\n- Private Libraries accessible only to certain groups of users.\n- Reads CBZ, CBR, CBT, and PDF formatted comics.\n- Syndication with OPDS, streaming, search and authentication.\n\n### Examples\n\n- _Filter by_ Story Arc and Unread, _Order by_ Publish Date to create an event\n  reading list.\n- _Filter by_ Unread and _Order by_ Added Time to see your latest unread comics.\n- _Search by_ your favorite character to find their appearances across different\n  comics.\n\n## <a name="demonstration">👀 Demonstration</a>\n\nYou may browse a [live demo server](https://codex.sl8r.net/) to get a feel for\nCodex.\n\n## <a name="news">📜 News</a>\n\nCodex has a <a href="NEWS.md">NEWS file</a> to summarize changes that affect\nusers.\n\n## <a name="installation">📦 Installation</a>\n\n### Install & Run with Docker\n\nRun the official [Docker Image](https://hub.docker.com/r/ajslater/codex).\nInstructions for running the docker image are on the Docker Hub README. This is\nthe recommended way to run Codex.\n\nYou\'ll then want to read the [Administration](#administration) section of this\ndocument.\n\n### Install & Run as a Native Application\n\nYou can also run Codex as a natively installed python application with pip.\n\n#### Wheel Build Dependencies\n\nYou\'ll need to install these system dependencies before installing Codex.\n\n##### macOS\n\n```sh\nbrew install jpeg libffi libyaml libzip openssl poppler python unrar webp\n```\n\n##### Linux\n\n###### <a href="#debian">Debian</a>\n\nLike Ubuntu, Mint, MX and others.\n\n```sh\napt install build-essential libffi-dev libjpeg-dev libssl-dev libwebp7 poppler-utils python3-pip zlib1g-dev\n```\n\nolder releases may use the `libweb6` package instead.\n\n###### Debian on ARM\n\nThe python cryptography wheel needs compiling on rare architectures. Install the\nRust compiler.\n\n```sh\napt install cargo\n```\n\n###### Alpine\n\n```sh\napk add bsd-compat-headers build-base jpeg-dev libffi-dev libwebp openssl-dev poppler-utils yaml-dev zlib-dev\n```\n\n##### Install unrar Runtime Dependency on Linux\n\nCodex requires unrar to read cbr formatted comic archives. Unrar is often not\npackaged for Linux, but here are some instructions:\n[How to install unrar in Linux](https://www.unixtutorial.org/how-to-install-unrar-in-linux/)\n\nUnrar as packaged for Alpine Linux v3.14 seems to work on Alpine v3.15\n\n#### Windows\n\nWindows users should use Docker to run Codex until this documentation section is\ncomplete.\n\nCodex can _probably_ run using Cygwin or the Windows Linux Subsystem but I\nhaven\'t done it yet. Contributions to this documentation accepted on\n[the outstanding issue](https://github.com/ajslater/codex/issues/76) or discord.\n\n##### Windows Linux Subsystem\n\nUntested. Try following the instructions for [Debian](#debian) above.\n\n##### Cygwin\n\nUntested partial instructions for the brave.\n\n1. Install [Cygwin](https://www.cygwin.com/).\n2. Install wget with cygwin.\n3. Install:\n   - python3.9+\n   - gcc\n   - gcc-g++\n   - libffi-devel\n   - libjpeg-devel\n   - libssl-devel\n   - mpfr\n   - mpc\n   - python3-devel\n   - python39-cffi\n   - python3.9-openssl with cygwin.\n4. Using a terminal:\n\n```sh\npip install wheel\n```\n\n#### Install Codex with pip\n\nYou may now install Codex with pip\n\n```sh\npip3 install codex\n```\n\n#### Run Codex Natively\n\npip should install the codex binary on your path. Run\n\n```sh\ncodex\n```\n\nand then navigate to <http://localhost:9810/>\n\n## <a name="administration">👑 Administration</a>\n\n### Navigate to the Admin Panel\n\n- Click the hamburger menu ☰ to open the browser settings drawer.\n- Log in as the \'admin\' user. The default administrator password is also\n  \'admin\'.\n- Navigate to the Admin Panel by clicking on its link in the browser settings\n  drawer after you have logged in.\n\n### Change the Admin password\n\nThe first thing you should do is log in as the admin user and change the admin\npassword.\n\n- Navigate to the Admin Panel as described above.\n- Select the Users tab.\n- Change the admin user\'s password using the small lock button.\n- You may also change the admin user\'s name with the edit button.\n- You may create other users and grant them admin privileges by making them\n  staff.\n\n### Add Comic Libraries\n\nThe second thing you will want to do is log in as an Administrator and add one\nor more comic libraries.\n\n- Navigate to the Admin Panel as described above.\n- Select the Libraries tab in the Admin Panel\n- Add a Library with the "+ LIBRARY" button in the upper left.\n\n### Reset the admin password\n\nIf you forget all your superuser passwords, you may restore the original default\nadmin account by running codex with the `CODEX_RESET_ADMIN` environment variable\nset.\n\n```sh\nCODEX_RESET_ADMIN=1 codex\n```\n\nor, if using Docker:\n\n```sh\ndocker run -e CODEX_RESET_ADMIN=1 -v <host path to config>/config:/config ajslater/codex\n```\n\n### Private Libraries\n\nIn the Admin Panel you may configure private libraries that are only accessible\nto specific groups.\n\nA library with _no_ groups is accessible to every user including anonymous\nusers.\n\nA library with _any_ groups is accessible only to users who are in those groups.\n\nUse the Groups admin panel to create groups and the Users admin panel to add and\nremove users to groups.\n\n### PDFs\n\nCodex only reads PDF metadata from the filename. If you decide to include PDFs\nin your comic library, I recommend taking time to rename your files so Codex can\nfind some metadata. Codex recognizes several file naming schemes. This one has\ngood results:\n\n`{series} v{volume} #{issue} {title} ({year}) {ignored}.pdf`\n\n## <a name="configuration">⚙️ Configuration</a>\n\n### Config Dir\n\nThe default config directory is `config/` directly under the working directory\nyou run codex from. You may specify an alternate config directory with the\nenvironment variable `CODEX_CONFIG_DIR`.\n\nThe config directory contains a file named `hypercorn.toml` where you can\nspecify ports and bind addresses. If no `hypercorn.toml` is present Codex copies\na default one to that directory on startup.\n\nThe default values for the config options are:\n\n```toml\nbind = ["0.0.0.0:9810"]\nquick_bind = ["0.0.0.0:9810"]\nroot_path = "/codex"\nmax_db_ops = 100000\n\n```\n\nThe config directory also holds the main sqlite database, the Whoosh search\nindex, a Django cache and comic book cover thumbnails.\n\n### Environment Variables\n\n- `LOGLEVEL` will change how verbose codex\'s logging is. Valid values are\n  `ERROR`, `WARNING`, `INFO`, `VERBOSE`, `DEBUG`. The default is `INFO`.\n- `TIMEZONE` or `TZ` will explicitly the timezone in long format (e.g.\n  `"America/Los Angeles"`). This is useful inside Docker because codex cannot\n  automatically detect the host machine\'s timezone.\n- `CODEX_CONFIG_DIR` will set the path to codex config directory. Defaults to\n  `$CWD/config`\n- `CODEX_RESET_ADMIN=1` will reset the admin user and its password to defaults\n  when codex starts.\n- `CODEX_SKIP_INTEGRITY_CHECK=1` will skip the database integrity repair that\n  runs when codex starts.\n- `CODEX_LOG_DIR` sets a custom directory for saving logfiles. Defaults to\n  `$CODEX_CONFIG_DIR/logs`\n- `CODEX_LOG_TO_FILE=0` will not log to files.\n- `CODEX_LOG_TO_CONSOLE=0` will not log to the console.\n\n### Reverse Proxy\n\n[nginx](https://nginx.org/) is often used as a TLS terminator and subpath proxy.\n\nHere\'s an example nginx config with a subpath named \'/codex\'.\n\n```nginx\n    # HTTP\n    proxy_set_header  Host              $http_host;\n    proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;\n    proxy_set_header  X-Forwarded-Host  $server_name;\n    proxy_set_header  X-Forwarded-Port  $server_port;\n    proxy_set_header  X-Forwarded-Proto $scheme;\n    proxy_set_header  X-Real-IP         $remote_addr;\n    proxy_set_header  X-Scheme          $scheme;\n\n    # Websockets\n    proxy_http_version 1.1;\n    proxy_set_header Upgrade $http_upgrade;\n    proxy_set_header Connection "Upgrade"\n\n    # This example uses a docker container named \'codex\' at sub-path /codex\n    # Use a valid IP or resolvable host name for other configurations.\n    location /codex {\n        proxy_pass  http://codex:9810;\n        # Codex reads http basic authentication.\n        # If the nginx credentials are different than codex credentials use this line to\n        #   not forward the authorization.\n        proxy_set_header Authorization "";\n    }\n```\n\nSpecify a reverse proxy sub path (if you have one) in `config/hypercorn.toml`\n\n```toml\nroot_path = "/codex"\n\n```\n\n#### Nginx Reverse Proxy 502 when container refreshes\n\nNginx requires a special trick to refresh dns when linked Docker containers\nrecreate. See this\n[nginx with dynamix upstreams](https://tenzer.dk/nginx-with-dynamic-upstreams/)\narticle.\n\n## <a name="usage">📖 Usage</a>\n\n### Sessions & Accounts\n\nOnce your administrator has added some comic libraries, you may browse and read\ncomics. Codex will remember your preferences, bookmarks and progress in the\nbrowser session. Codex destroys anonymous sessions and bookmarks after 60 days.\nTo preserve these settings across browsers and after sessions expire, you may\nregister an account with a username and password. You will have to contact your\nadministrator to reset your password if you forget it.\n\n### ᯤ OPDS\n\nCodex supports OPDS syndication and OPDS streaming. You may find the OPDS url in\nthe side drawer. It should take the form:\n\n`http(s)://host.tld(:9810)(/root_path)/opds/v1.2/`\n\n#### Clients\n\n- iOS has [Panels](https://panels.app/), [KYBook 3](http://kybook-reader.com/),\n  and\n  [Chunky Comic Reader](https://apps.apple.com/us/app/chunky-comic-reader/id663567628)\n- Android has\n  [Moon+](https://play.google.com/store/apps/details?id=com.flyersoft.moonreader)\n  and\n  [Librera](https://play.google.com/store/apps/details?id=com.foobnix.pdf.reader)\n\n#### HTTP Basic Authentication\n\nIf you wish to access OPDS as your Codex User. You will have to add your\nusername and password to the URL. Some OPDS clients do not asssist you with\nauthentication. In that case the OPDS url will look like:\n\n`http(s)://username:password@host.tld(:9810)(/root_path)/opds/v1.2/`\n\n#### Supported OPDS Specifications\n\n- OPDS 1.2\n- OPDS-PSE 1.1\n- OPDS Authentication 1.0\n- OpenSearch\n\n## <a name="troubleshooting">🩺 Troubleshooting</a>\n\n### Logs\n\nCodex collects its logs in the `config/logs` directory. Take a look to see what\nth e server is doing.\n\nYou can change how much codex logs by setting the `LOGLEVEL` environment\nvariable. By default this level is `INFO`. To see more messages run codex like:\n\n```bash\nLOGLEVEL=VERBOSE codex\n```\n\nTo see a great deal of noisy messages from dependencies try:\n\n```bash\nLOGLEVEL=DEBUG codex\n```\n\n### Watching Filesystem Events with Docker\n\nCodex tries to watch for filesystem events to instantly update your comic\nlibraries when they change on disk. But these native filesystem events are not\ntranslated between macOS & Windows Docker hosts and the Docker Linux container.\nIf you find that your installation is not updating to filesystem changes\ninstantly, you might try enabling polling for the affected libraries and\ndecreasing the `poll_every` value in the Admin console to a frequency that suits\nyou.\n\n### Emergency Database Repair\n\nIf the database becomes corrupt, Codex includes a facitlity to rebuild the\ndatabase. Place a file named `rebuild_db` in your Codex config directory like\nso:\n\n```sh\n  touch config/rebuild_db\n```\n\nShut down and restart Codex.\n\nThe next time Codex starts it will back up the existing database and try to\nrebuild it. The database lives in the config directory as the file\n`config/db.sqlite3`. If this procedure goes kablooey, you may recover the\noriginal database at `config/db.sqlite3.backup`.\n\n### Bulk Database Updates Fail\n\nI\'ve tested Codex\'s bulk database updater to batch 100,000 filesystem events at\na time. With enough RAM Codex could probably batch much more. But if you find\nthat updating large batches of comics are failing, consider setting a the\n`max_db_ops` value in `hypercorn.toml` to a lower value. 1000 will probably\nstill be pretty fast, for instance.\n\n### 🐛 Bug Reports\n\nIssues and feature requests are best filed on the\n[Github issue tracker](https://github.com/ajslater/codex/issues).\n\nBy the generosity of the good people of\n[Mylar](https://github.com/mylar3/mylar3), I and other Codex users may be found\nanswering questions on the [Mylar Discord](https://discord.gg/6UG94R7E8T).\nPlease use the `#codex-support` channel to ask for help with Codex.\n\n## <a name="out-of-scope">🚫 Out of Scope</a>\n\n- I have no intention of making this an eBook reader.\n- I think metadata editing would be better placed in a comic manager than a\n  reader.\n\n## <a name="alternatives-to-codex">📚Alternatives</a>\n\n- [Kavita](https://www.kavitareader.com/) has light metadata filtering/editing,\n  supports comics, eBooks, and features for manga.\n- [Komga](https://komga.org/) has light metadata editing.\n- [Ubooquity](https://vaemendis.net/ubooquity/) reads both comics and eBooks.\n- [Mylar](https://github.com/mylar3/mylar3) is the best comic book manager which\n  also has a built in reader.\n- [Comictagger](https://github.com/comictagger/comictagger) is a comic metadata\n  editor. It comes with a powerful command line and desktop GUI.\n\n## <a name="develop-codex">🛠 Develop</a>\n\nCodex is a Django Python webserver with a VueJS front end.\n\n`/codex/codex/` is the main django app which provides the webserver and\ndatabase.\n\n`/codex/frontend/` is where the vuejs frontend lives.\n\n`/codex/dev-env-setup.sh` will install development dependencies.\n\n`/codex/dev-ttabs.sh` will run the three or four different servers recommended\nfor development in terminal tabs.\n\n`/codex/dev-codex.sh` runs the main Django server. Set the `DEBUG` environment\nvariable to activate debug mode: `DEBUG=1 ./run.sh`. This also lets you run the\nserver without collecting static files for production and with a hot reloading\nfrontend. I recommend setting `LOGLEVEL=VERBOSE` for development as well.\n\n`/codex/frontend/dev-server.sh` runs the development autoreloading frontend with\nvite.\n\n### Links\n\n- [Docker Image](https://hub.docker.com/r/ajslater/codex)\n- [PyPi Package](https://pypi.org/project/codex/)\n- [GitHub Project](https://github.com/ajslater/codex/)\n\n## <a name="special-thanks">🙏🏻 Special Thanks</a>\n\n- Thanks to [Aurélien Mazurie](https://pypi.org/user/ajmazurie/) for allowing me\n  to use the PyPi name \'codex\'.\n- Thanks to the good people of\n  [#mylar](https://github.com/mylar3/mylar3#live-support--conversation) for\n  continuous feedback and comic ecosystem education.\n\n## <a name="enjoy">😊 Enjoy</a>\n\n![These simple people have managed to tap into the spiritual forces that mystics and yogis spend literal lifetimes seeking. I feel... ...I feel...](strange.jpg)\n',
    'author': 'AJ Slater',
    'author_email': 'aj@slater.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ajslater/codex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
