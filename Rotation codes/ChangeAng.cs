using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

public class ChangeAng : MonoBehaviour
{
    static Socket listener;
    private CancellationTokenSource source;
    public ManualResetEvent allDone;
    public Renderer objectRenderer;
    //Vector3 pos = Vector3.zero;
    Vector3 rot = Vector3.zero;

    public static readonly int PORT = 1755;
    public static readonly int WAITTIME = 5;


    ChangeAng()
    {
        source = new CancellationTokenSource();
        allDone = new ManualResetEvent(false);
    }

    // Start is called before the first frame update
    async void Start()
    {
        objectRenderer = GetComponent<Renderer>();
        await Task.Run(() => ListenEvents(source.Token));   
    }

    // Update is called once per frame
    void Update()
    {
        //transform.position = pos;
        transform.rotation = Quaternion.Euler(rot);
    }

    private void ListenEvents(CancellationToken token)
    {

        
        IPHostEntry ipHostInfo = Dns.GetHostEntry(Dns.GetHostName());
        IPAddress ipAddress = ipHostInfo.AddressList.FirstOrDefault(ip => ip.AddressFamily == AddressFamily.InterNetwork);
        //IPAddress ipAddress = 192.168.0.154;
        IPEndPoint localEndPoint = new IPEndPoint(ipAddress, PORT);
        

         
        listener = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

         
        try
        {
            listener.Bind(localEndPoint);
            listener.Listen(10);

             
            while (!token.IsCancellationRequested)
            {
                allDone.Reset();

                print("Waiting for a connection... host :" + ipAddress.MapToIPv4().ToString() + " port : " + PORT);
                listener.BeginAccept(new AsyncCallback(AcceptCallback),listener);

                while(!token.IsCancellationRequested)
                {
                    if (allDone.WaitOne(WAITTIME))
                    {
                        break;
                    }
                }
      
            }

        }
        catch (Exception e)
        {
            print(e.ToString());
        }
    }

    void AcceptCallback(IAsyncResult ar)
    {  
        Socket listener = (Socket)ar.AsyncState;
        Socket handler = listener.EndAccept(ar);
 
        allDone.Set();
  
        StateObject state = new StateObject();
        state.workSocket = handler;
        handler.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReadCallback), state);
    }

    void ReadCallback(IAsyncResult ar)
    {
        StateObject state = (StateObject)ar.AsyncState;
        Socket handler = state.workSocket;

        int read = handler.EndReceive(ar);
  
        if (read > 0)
        {
            state.locationCode.Append(Encoding.ASCII.GetString(state.buffer, 0, read));
            handler.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReadCallback), state);
        }
        else
        {
            if (state.locationCode.Length > 1)
            { 
                string content = state.locationCode.ToString();
                print($"Read {content.Length} bytes from socket.\n Data : {content}");
                rot = 1f * sTv(content);
                //SetLocation(content);
            }
            handler.Close();
        }
    }

    //Set location
    public Vector3 sTv (string data) 
    {
        string[] Location = data.Split(',');

        // store as a Vector3
        Vector3 result = new Vector3(
            float.Parse(Location[0]),
            float.Parse(Location[1]),
            float.Parse(Location[2]));
        
        return result;

    }
    /*private void SetLocation (string data) 
    {
        string[] Location = data.Split(',');
        pos = new Location()
        {
            x = float.Parse(sArray[0]),
            y = float.Parse(sArray[1]),
            z = float.Parse(sArray[3])
        };

    }
    */

    private void OnDestroy()
    {
        source.Cancel();
    }

    public class StateObject
    {
        public Socket workSocket = null;
        public const int BufferSize = 1024;
        public byte[] buffer = new byte[BufferSize];
        public StringBuilder locationCode = new StringBuilder();
    }
}
