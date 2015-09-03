unit Img_serv;
// img_client_pi.py

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, IdContext, Vcl.StdCtrls,
  IdBaseComponent, IdComponent, IdCustomTCPServer, IdTCPServer, Vcl.ExtCtrls;

type
  TForm1 = class(TForm)
    IdTCPServer1: TIdTCPServer;
    Memo1: TMemo;
    Image1: TImage;
    procedure IdTCPServer1Execute(AContext: TIdContext);
    procedure FormCreate(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.dfm}

procedure TForm1.FormCreate(Sender: TObject);
begin
  IdTCPServer1.Active := True;
end;

procedure TForm1.IdTCPServer1Execute(AContext: TIdContext);
var
  img_l: longword; // unsigned 32 bit
  Strm: TStream;
begin
  Strm := TMemoryStream.Create;
  //Strm := TFileStream.Create('c:\data\test.bmp', fmOpenReadWrite);
  Strm := TMemoryStream.Create;

  img_l := AContext.Connection.Socket.ReadLongWord();

  memo1.Lines.Add( inttostr(img_l) );

  while img_l > 0 do begin
    Strm.Position := 0;
    AContext.Connection.Socket.ReadStream(Strm, img_l);
    memo1.Lines.Add( 'Strm' );
    //Strm.Free;
    Strm.Position := 0;
    //Image1.Picture.LoadFromFile('c:\data\test.bmp');
    Image1.Picture.Bitmap.LoadFromStream(strm);

    img_l := AContext.Connection.Socket.ReadLongWord();
    memo1.Lines.Add( inttostr(img_l) );

  end;

  memo1.Lines.Add('Discon');
  AContext.Connection.Disconnect;
end;

{var
  sName: String;
begin
  // Send command to client immediately after connection
  AContext.Connection.Socket.WriteLn('What is your name?');
  // Receive response from client
  sName := AContext.Connection.Socket.ReadLn;
  // Send a response to the client
  AContext.Connection.Socket.WriteLn('Hello, ' + sName + '.');
  AContext.Connection.Socket.WriteLn('Would you like to play a game?');
  // We're done with our session
  AContext.Connection.Disconnect;
end;}

end.
