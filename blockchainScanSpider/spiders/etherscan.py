import os
import scrapy
import logging

class EtherscanSpider(scrapy.Spider):
    name = "etherscan"
    
    allowed_domains = ["etherscan.io"]

    def start_requests(self):
        url       = "https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7#code"
        # url       = "https://etherscan.io/token/0x6921c63fcf9796c9733690804e116be3520ba468#code"
        yield scrapy.Request(url, self.parseCode)

    def parseCode(self, response):

        # 部署名
        deployName    = response.xpath('//*[@id="ContentPlaceHolder1_contractCodeDiv"]/div[2]/div[1]/div[1]/div[2]/span/text()').extract_first()

        # 代码文件数量
        editorCount   = response.xpath('count(//*[starts-with(@id, "editor")])')[0].extract()
        editorCount   = int(float(editorCount))
        # 代码列表
        editors       = response.xpath('//*[starts-with(@id, "editor")]')
        # 输出位置
        baseDir =  'project/'

        if (editorCount > 1):
            # 多个文件
            for editor in editors:
                # 文件
                file = editor.xpath('preceding-sibling::div[1]/span/text()').extract_first()
                file = baseDir + file.split(":")[-1].strip()
                # 代码
                code = editor.xpath('text()').extract_first()
                # 写入文件
                with open(file, "w") as f:
                    f.write(code) 
        else :
            # 单个文件
            # 文件
            file = baseDir + deployName + '.sol'
            # 代码
            code = editors.xpath('text()').extract_first()
            # 写入文件
            with open(file, "w") as f:
                f.write(code)
