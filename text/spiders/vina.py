import scrapy
from scrapy_splash import SplashRequest
import requests


def script(n):
    _script = """
        function main(splash)
            splash.private_mode_enabled = false
            splash: set_viewport_full()
            assert (splash:go(args.url))
            assert (splash:wait(2))
            local button = splash:select('.btn-style')
            button:mouse_click()
            splash:wait(2)
            button = splash:select('div.list-promotion-item:nth-child({})')
            button: mouse_click()
            splash: wait(1)
          return {}
        end
        """.format('''
        html = splash:html(),
        png = splash:png(),
        har = splash:har(),
        ''',n)
    return _script


class VinaSpider(scrapy.Spider):
    name = 'vina'
    start_urls = ['https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/5/0/-1']
    # start_urls = [
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/1/0/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/1/21/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/1/2/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/1/3/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/1/4/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/2/0/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/2/21/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/2/2/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/2/3/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/2/4/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/3/0/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/3/21/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/3/2/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/3/4/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/4/0/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/4/21/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/4/2/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/4/4/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/5/0/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/5/21/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/5/2/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/5/4/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/QuaTang/1/0/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/QuaTang/2/0/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/DoiDiem/3/0/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/DoiDiem/3/16/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/DoiDiem/3/15/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/DoiDiem/3/14/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/DoiDiem/5/0/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/DoiDiem/5/7/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/DoiDiem/5/2/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/DoiDiem/5/3/-1',
        # 'https://vinaphoneplus.com.vn/#/main/list/DoiDiem/5/4/-1',
    # ]

    header = {'Accept': 'application/json, text/plain, */*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
              'Connection': 'keep-alive',
              'Content-Length': 0,
              # Cookie: _ga=GA1.3.2076927145.1598422558; _gid=GA1.3.645300138.1598422558; _pk_id.328.9060=b6eeaeac8b06eadd.1598597528.1.1598597528.1598597528.
              'Host': 'apiquantri.vinaphoneplus.com.vn',
              'Origin': 'https://vinaphoneplus.com.vn',
              'Referer': 'https://vinaphoneplus.com.vn/',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-site',
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36', }

    def parse(self, response):
        script = '''
            function main(splash, args)
              splash.private_mode_enabled = false
              splash: set_viewport_full()
              assert (splash:go(args.url))
              assert (splash:wait(0.5))
              local button = splash:select('.btn-style')
              button:mouse_click()
              splash:wait(0.5)
            
              buttons = splash:select_all('.list-promotion-item')
              -- buttons = splash:select('div.list-promotion-item:nth-child(2)')
              --assert(splash:runjs("$('#title.play-ball > a:first-child').click()"))
            
              arr = {}
            
              for i,button in ipairs(buttons) do
                --c = splash:select('div.list-promotion-item:nth-child(i)')
                button:mouse_click()
                splash:wait(0.5)
                exit = splash:select('body > div.modal.fade.ng-isolate-scope.in > div > div > div.modal-header > img')
                exit:mouse_click()
                splash:wait(0.5)
                
              end
            
            
              return {
                html = splash:html(),
                png = splash:png(),
                har = splash:har(),
              }
            end
            '''

        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse_annoucement,
                                endpoint='execute',
                                args={'lua_source': script,
                                      'url': url,
                                      'header': self.header
                                      })

        #     for item in items do
        #     item: mouse_click()
        #     splash.wait(0.5)
        # end


    # local
    # button = splash:select('div.list-promotion-item:nth-child(2)')
    # button: mouse_click()
    # splash: wait(1)

    def parse_annoucement(self, response):
        har_parser = response.data['har']
        for i in range(len(har_parser['log']['entries'])):
            s = har_parser['log']['entries'][i]['request']['url']
            if 'Api_XemThongTinChuongTrinhUuDai' in s:
                response = requests.get(s,verify = False)
                print(response.text.encode('utf-8').decode("utf-8"))


