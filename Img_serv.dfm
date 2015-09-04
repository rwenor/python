object Form1: TForm1
  Left = 0
  Top = 0
  Caption = 'Form1'
  ClientHeight = 459
  ClientWidth = 480
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 13
  object Image1: TImage
    Left = 8
    Top = 128
    Width = 465
    Height = 321
    Proportional = True
    Stretch = True
  end
  object Memo1: TMemo
    Left = 8
    Top = 16
    Width = 449
    Height = 89
    Lines.Strings = (
      'Memo1')
    TabOrder = 0
  end
  object IdTCPServer1: TIdTCPServer
    Bindings = <
      item
        IP = '0.0.0.0'
        Port = 8000
      end>
    DefaultPort = 8000
    OnExecute = IdTCPServer1Execute
    Left = 32
    Top = 16
  end
end
