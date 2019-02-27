import docker
import argparse
import sys
import os

client = docker.from_env()
config_ = {
    'working_dir': '/usr',
    'volumes': {'/Users/mac/development/Docker-projects/docker-compose/usr/new_project/spiders/json': {'bind': '/usr/json', 'mode': 'rw'}},
    'auto_remove': True}


def container_creator(img, spider):
    new_container = None
    try:
        new_container = client.containers.create(image=img, working_dir=config_['working_dir'],
                                                 command='scrapy runspider ' + spider + ".py" + " -o json/" + spider + ".json",
                                                 auto_remove=config_['auto_remove'], volumes=config_['volumes'])
    except docker.errors.ImageNotFound:
        print("Specified image does not exist")
    except docker.errors.APIError:
        print("Server returns an error")
    return new_container


def parser_args():
    result = None
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('template', nargs=1, type=str, help="Template filename")
        parser.add_argument('domain', nargs=1, type=str, help="Domain")
        args = parser.parse_args()
        template = args.template[0]
        domain = args.domain[0]
        domain_under = domain.replace(".", "_")
        result = {'template': template, 'domain': domain, 'domain_under': domain_under}
    except SystemExit:
        pass
    return result


def copy_spider_file(container_id, spider_file):
    out = False
    copying = os.popen("docker cp ../spiders/" + spider_file + " " + container_id + ":usr/")
    res = copying.close()
    if res is None:
        print("\nSpider file transfer to container completed successfully")
        out = True
    else:
        print("Copying spider file -> Error code " + str(res))
    return out


def create_spider_file(template, domain):
    temp = template + ".py"
    dom = domain
    dom_under = dom.replace(".", "_")
    spider_file_name = dom_under + '.py'
    if not os.path.isfile('../spiders/' + dom_under + '.py'):
        file = open("../templates/" + temp, 'r+')
        temp_py = file.read()
        temp_py = temp_py.replace("{domain}", dom).replace("{domain_under}", dom_under)
        file.close()
        try:
            new_py = open("../spiders/" + dom_under + ".py", mode='w')
            new_py.write(temp_py)
            new_py.close()
            print("Creating new configuration file for job - done")
            spider_file_name = new_py.name
        except IOError:
            print("Can't create new configuration file for job")
        return spider_file_name
    else:
        print("\nSpider file is already exist")
        return spider_file_name


parsed = parser_args()

if parsed:
    new_cont = container_creator('04db5ec97f7d', parsed['domain_under'])
    container_id = new_cont.id[:12]
    spider_file = create_spider_file(parsed['template'], parsed['domain'])
    if spider_file is not None:
        copy_result = copy_spider_file(container_id, spider_file)
        if copy_result:
            new_cont.start()
            print("\nDocker container was started -> id: " + container_id +
                  "\n===> running scrapy spider " + spider_file)
