import click
import re

@click.command()
@click.option('--options', default="hps", help='number of greetings')
@click.option('--function', default="null", help='number of greetings')
@click.argument('file', type=click.File('rb'))
def main(options, function, file):
    data = file.readlines()
    opts = list(options)
    if function == 'print':
        printFile(data)
    if function.lower() == 'livehosts':
        printBanner(opts)
        getLiveHosts(opts, data)
    if 'search-service' in function.lower():
        term = function.split("=")[1]
        printBanner(opts)
        searchServices(opts, term.lower(), data)
    if 'uniq-services' in function.lower():
        printBanner(["p","s"])
        uniqServices(opts, data)

def printFile(data):
    click.echo(data)

def printFunction(portsNservices, options):

        if all(o in options for o in ["h","p","s"]):
            for ps in portsNservices:
                click.echo("\t"+ps[0]+"\t ------ \t"+ps[1]+"\t ------ \t"+ps[2])
        elif all(o in options for o in ["h","p"]):
            for ps in portsNservices:
                click.echo("\t"+ps[0]+"\t ------ \t"+ps[1])
        elif all(o in options for o in ["h", "s"]):
            for ps in portsNservices:
                click.echo("\t"+ps[0]+"\t ------ \t"+ps[2])
        elif all(o in options for o in ["p","s"]):
            for ps in portsNservices:
                click.echo("\t"+ps[1]+"\t ------ \t"+ps[2])
        elif all(o in options for o in ["h"]):
            click.echo("\t"+ps[0])
        elif all(o in options for o in ["s"]):
            for ps in portsNservices:
                click.echo("\t"+ps[2])
        elif all(o in options for o in ["p"]):
            for ps in portsNservices:
                click.echo("\t"+ps[1])





def getLiveHosts(opts, data):
    list1 = []
    for line in data:
        if 'Host:'in line and 'Ports:' in line:

            for l in line.split("Ports: ")[1].split(", "):
                if '/open/' in l:
                    pair = (line.split("Host: ")[1].split(" ()")[0],l.split('/open/tcp//')[0],l.split('/open/tcp//')[1])
                    list1.append(pair)
    printFunction(list1, opts)
def searchServices(opts, searchTerm, data):
    list1 = []
    for line in data:
        if 'Host:'in line and 'Ports:' in line:

            for l in line.split("Ports: ")[1].split(", "):
                if '/open/' in l:
                    pair = (line.split("Host: ")[1].split(" ()")[0],l.split('/open/tcp//')[0],l.split('/open/tcp//')[1])
                    if searchTerm.lower() in pair[2].lower():
                        list1.append(pair)
    printFunction(list1, opts)

def uniqServices(opts, data):
    all_services = []
    uniq_services = []
    uniq = []

    for line in data:
        if 'Ports: ' in line:
            for port in line.split("Ports: ")[1].split(", "):
                if 'open' in port:
                    if 'Ignored State' in port:
                        all_services.append("\t"+port.replace("/open/tcp//", ": --------------- \t").replace("\n","").split("\tIgnored State:")[0])
                    else:
                        all_services.append("\t"+port.replace("/open/tcp//", ": --------------- \t").replace("\n",""))


    uniq = set(all_services)
    for service in uniq:
        uniq_services.append(service)
    uniq_services.sort(key=natural_keys)
    for service in uniq_services:
        click.echo(service)


def printBanner(options):
    if all(o in options for o in ["h","p","s"]):
        click.echo("\tHOST\t\t\t\tPORT\t\t\t\tSERVICE")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["h","p"]):
        click.echo("\tHOST\t\t\t\tPORT")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["h", "s"]):
        click.echo("\tHOST\t\t\t\tSERVICE")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["p","s"]):
        click.echo("\tPORT\t\t\t\tSERVICE")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["h"]):
        click.echo("\tHOST")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["s"]):
        click.echo("\tSERVICE")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["p"]):
        click.echo("\tPORT")
        click.echo("================================================================================================================")


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):

    return [ atoi(c) for c in re.split(':', text) ]


if __name__ == '__main__':
    main()