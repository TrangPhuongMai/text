import re
import scrapy
from scrapy_splash import SplashRequest
import requests
import html
import json
from scrapy.loader import ItemLoader
from text.items import TextItem


class VinaSpider(scrapy.Spider):
    name = 'vina'
    start_urls = [
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/1/0/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/1/21/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/1/2/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/1/3/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/1/4/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/2/0/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/2/21/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/2/2/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/2/3/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/2/4/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/3/0/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/3/21/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/3/2/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/3/4/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/4/0/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/4/21/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/4/2/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/4/4/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/5/0/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/5/21/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/5/2/-1",
        "https://vinaphoneplus.com.vn/#/main/list/HangHoiVien/5/4/-1",
        "https://vinaphoneplus.com.vn/#/main/list/QuaTang/1/0/-1",
        "https://vinaphoneplus.com.vn/#/main/list/QuaTang/2/0/-1",
        "https://vinaphoneplus.com.vn/#/main/list/DoiDiem/3/0/-1",
        "https://vinaphoneplus.com.vn/#/main/list/DoiDiem/3/16/-1",
        "https://vinaphoneplus.com.vn/#/main/list/DoiDiem/3/15/-1",
        "https://vinaphoneplus.com.vn/#/main/list/DoiDiem/3/14/-1",
        "https://vinaphoneplus.com.vn/#/main/list/DoiDiem/5/0/-1",
        "https://vinaphoneplus.com.vn/#/main/list/DoiDiem/5/7/-1",
        "https://vinaphoneplus.com.vn/#/main/list/DoiDiem/5/2/-1",
        "https://vinaphoneplus.com.vn/#/main/list/DoiDiem/5/3/-1",
        "https://vinaphoneplus.com.vn/#/main/list/DoiDiem/5/4/-1",
    ]

    def parse(self, response):
        script = '''
            function scroll_to(splash, x, y)
              local js = string.format("window.scrollTo(%s, %s);",
                tonumber(x),
                tonumber(y))
              return splash:runjs(js)
            end
            
            
            function get_doc_height(splash)
              return splash:runjs([[
                Math.max(
                Math.max(document.body.scrollHeight, document.getElementById("content").scrollHeight),
                Math.max(document.body.offsetHeight, document.getElementById("content").offsetHeight),
                Math.max(document.body.clientHeight, document.getElementById("content").clientHeight)
              )
              )
                ]])
            end
            
            function scroll_to_bottom(splash)
              local y = get_doc_height(splash)
              return scroll_to(splash, 0, y)
            end
                   
            
            
            
            function main(splash, args)
              
              
                  splash.private_mode_enabled = false
                  assert (splash:go(args.url))
                  assert (splash:wait(1))
                  splash:stop()
            
                  for i = 1, 5 do
                    scroll_to_bottom(splash)
                    assert(splash:wait(0.3))
                  end
            
                  splash:set_viewport_full()
                  assert (splash:wait(1.5))
                  local button = splash:select('.btn-style')
                  button:mouse_click()
                  splash:wait(1)
                
                  buttons = splash:select_all('.list-promotion-item')
                  -- buttons = splash:select('div.list-promotion-item:nth-child(2)')
                  --assert(splash:runjs("$('#title.play-ball > a:first-child').click()"))
            
                
                  for i,button in ipairs(buttons) do
                    --c = splash:select('div.list-promotion-item:nth-child(i)')
                    button:mouse_click()
                    splash:wait(1.5)
                    exit = splash:select('body > div.modal.fade.ng-isolate-scope.in > div > div > div.modal-header > img')
                    exit:mouse_click()
                    splash:wait(1)
                    
                  end
                
                
                  return {
                    html = splash:html(),
                    png = splash:png(),
                    har = splash:har(),
                  }
                end
            '''
        # l = ItemLoader(TextItem(), response=response)
        for url in self.start_urls:
            # l.add_value('url', url)

            yield SplashRequest(url=url,
                                callback=self.parse_annoucement,
                                # errback=self.error_parse,
                                endpoint='execute',
                                args={'lua_source': script,
                                      'url': url,
                                      # 'header': self.header,
                                      'timeout': 120,
                                      'wait': 0.5,
                                      },
                                meta={'url': url})



    def parse_annoucement(self, response):
        l = ItemLoader(TextItem(), response=response, )
        l.add_value('url', response.meta['url'])
        har_parser = response.data['har']
        for i in range(len(har_parser['log']['entries'])):
            s = har_parser['log']['entries'][i]['request']['url']
            if 'Api_XemThongTinChuongTrinhUuDai' in s:
                text = requests.get(s, verify=False)
                json_str = json.loads(text.content)
                json_str['data'][0][0]['MoTa'] = html.unescape(re.sub('<[^<]+?>', '', json_str['data'][0][0]['MoTa']))
                l.add_value('text', json_str['data'][0][0])

        yield l.load_item()
