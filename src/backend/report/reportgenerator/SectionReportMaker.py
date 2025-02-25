import glob
from pathlib import Path
import os
import re
from bs4 import BeautifulSoup
from bs4 import element


class SectionReportMaker:
    WORK_DIR: str

    def __init__(self, work_dir: str, summary_file: str, report_dataset: dict):
        self.WORK_DIR = work_dir
        self.SUMMARY_FILE = summary_file
        self.report_dataset = report_dataset

        self.REPLACE_STRING = {
            "<!--%%AUTHOR%%-->": self.make_author_AuthorOfReport,
            "<!--%%SECTION_TITLE_1%%-->": self.make_section_title,
            "<!--%%SECTION_TITLE_2%%-->": self.make_section_title,
            "<!--%%SECTION_TITLE_3%%-->": self.make_section_title,
            "<!--%%SECTION_TITLE_4%%-->": self.make_section_title,
            "<!--%%SECTION_TITLE_5%%-->": self.make_section_title,
            "<!--%%SECTION_TITLE_6%%-->": self.make_section_title,
            "<!--%%SECTION_TITLE_7%%-->": self.make_section_title,
            "<!--%%SECTION_TITLE_8%%-->": self.make_section_title,
            "<!--%%SECTION_1%%-->": self.make_section,
            "<!--%%SECTION_2%%-->": self.make_section,
            "<!--%%SECTION_3%%-->": self.make_section,
            "<!--%%SECTION_4%%-->": self.make_section,
            "<!--%%SECTION_5%%-->": self.make_section,
            "<!--%%SECTION_6%%-->": self.make_section,
            "<!--%%SECTION_7%%-->": self.make_section,
            "<!--%%SECTION_8%%-->": self.make_section,
            "<!--%%SUMMARY%%-->": self.make_summary_SummaryOfTestResult,
            "<!--%%DATE%%-->": self.make_date_DateOfReportGenerated,
            "<!--%%MLCOMPONENT_NAME%%-->": self.make_ml_component_name_NameOfProduct,
            "<!--%%TEST_ENVIRONMENT%%-->": self.make_testenvironment_EnvironmentOfTest
        }

    def collation_replacement_str(self, replace_mark: str):
        print('SectionReportMaker() collation_replacement_str() start')
        try:
            html_iframe = ""
            make_method = self.REPLACE_STRING.get(replace_mark)
            if make_method is None:
                # 非対応の拡張子のエラー、またはファイルが存在しない
                print(replace_mark)
            else:
                chapter = re.sub("\\D", "", replace_mark)
                if chapter:
                    html_iframe = make_method(chapter)
                else:
                    html_iframe = make_method()
        except Exception as e:
            raise e
        return html_iframe

    def make_section_title(self, chapter: str):
        qd_value = self.report_dataset['QualityDimension'][chapter]
        # TODO:QualityDimensionのリンクを管理するカラムが存在しない(M_TestRunnerのqualityを見ればわかる)が固定でも問題ないか
        # TODO:QualityDimensionのリンクをレポートに出力するフォーマットは要検討
        # landing_page = 'https://airc.aist.go.jp/aiqm/quality/internal/' + qd_value
        # html_iframe = "<span> " + qd_value + " " + landing_page + " </span>\n"
        html_iframe = "<span> " + qd_value + " </span>\n"
        return html_iframe

    def make_author_AuthorOfReport(self):
        html_iframe = \
            "<span> " + self.report_dataset['Author'] + "</span>\n"
        return html_iframe

    def make_summary_SummaryOfTestResult(self):
        html_iframe = ""
        path = Path(self.SUMMARY_FILE)
        relative_path = str(path.relative_to(path.parent.parent))
        html_iframe += \
            "<iframe id=\"summary_frame\" src=" + relative_path + \
            " scrolling=\"no\" frameborder=\"0\" class=\"frame\"></iframe>\n"
        return html_iframe

    def make_date_DateOfReportGenerated(self):
        html_iframe = \
            "<span> " + self.report_dataset['Date'] + "</span>\n"
        return html_iframe

    def make_ml_component_name_NameOfProduct(self):
        html_iframe = \
            "<span> " + self.report_dataset['MLComponentName'] + "</span>\n"
        return html_iframe

    def make_testenvironment_EnvironmentOfTest(self):
        test_environment = self.report_dataset['TestEnvironment']
        inner_html = \
            '''
            <tr>
              <td>CPU Brand</td>
              <td>{}</td>
            </tr>
            <tr>
              <td>CPU Architecture</td>
              <td>{}</td>
            </tr>
            <tr>
              <td>CPU Clocks</td>
              <td>{}</td>
            </tr>
            <tr>
              <td>CPU Cores</td>
              <td>{}</td>
            </tr>
            <tr>
              <td>Memory Capacity</td>
              <td>{}</td>
            </tr>
            '''.format(
                test_environment['cpu_brand'],
                test_environment['cpu_arch'],
                test_environment['cpu_clocks'],
                test_environment['cpu_cores'],
                self.__convert_unit(int(test_environment['memory_capacity']), 1)
            )
        return inner_html

    def make_section(self, chapter: str):
        html_iframe = ""
        html_list = glob.glob(self.WORK_DIR + chapter + os.sep + "*.html")
        for html_file in html_list:
            path = Path(html_file)
            html_iframe += \
                self._get_td_body(path) + \
                "<div class=\"page-break-before\"></div>\n"

        return html_iframe

    @staticmethod
    def _get_td_body(html_path: Path):
        td_body = ''
        with open(str(html_path), encoding="utf-8_sig") as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')

            # srcパス書き換え
            parent_name = html_path.parent.name
            for i in soup.find_all("iframe"):
                i["src"] = parent_name + os.sep + i.get("src")

            # body取得
            for body_tag in soup.body.contents:
                if type(body_tag) is element.Tag:
                    td_body += str(body_tag) + '\n'

        return td_body

    def __convert_unit(self, raw_byte: int, decimal_place: int):
        unit_list = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

        raw_byte_clone = raw_byte
        i = -1
        while(raw_byte_clone > 0):
            raw_byte_clone = raw_byte_clone//1024
            i += 1
        
        s = '{} {}'.format(
            round(raw_byte/(1024**i), decimal_place), 
            unit_list[i]
        )
        return s