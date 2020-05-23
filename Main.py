from time import sleep

from freelancer_project.libs.host import Host
from freelancer_project.libs.host import check_connection
from freelancer_project.libs.manage_yaml import open_yaml
from freelancer_project.libs.read_excel import write_to_excel


class Main:

    def __init__(self):
        self.user = input('Username: ')
        self.password = input('Password: ')
        self.yaml = open_yaml()
        self.host = Host()
        self.max_tries_connection = 3

    def open_freelancer_website(self):
        url = self.yaml['freelancer_page']['url_1']

        while self.max_tries_connection > 0:
            response = check_connection(url)

            # Check if site is up and running
            if not response[0]:
                print('Error connecting to page. Response was ' + str(response[1]))
                self.max_tries_connection -= 1
                self.host.close_browser()
                continue

            self.host.open_browser()
            self.host.go_to_page(url)
            self.host.login_page(self.user, self.password)

            if self.host.verify_page(self.yaml['main_page']['main_page_title']):
                break
            else:
                self.max_tries_connection -= 1
                self.host.close_browser()

    def search_projects(self, criteria: str):
        self.host.go_to_page(self.yaml['freelancer_page']['url_2'])
        self.host.search_projects(criteria)

    def get_available_projects_list(self):
        return self.host.get_projects_list()

    def write_projects_to_file(self, projects):
        write_to_excel(projects)

    def clean_up(self):
        self.host.close_browser()


if __name__ == '__main__':
    m = Main()
    m.open_freelancer_website()
    m.search_projects('scrap')
    sleep(5)
    projects = m.get_available_projects_list()
    write_to_excel(projects)
    m.clean_up()
