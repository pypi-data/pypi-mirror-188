package Javonet::Core::Transmitter::PerlTransmitterWrapper;
use utf8;
use warnings;
use strict;
use lib 'lib';
use FFI::Platypus;
use Path::Tiny;
use Exporter;
use File::Spec;
my $ffi;

our @ISA = qw(Exporter);
our @EXPORT = qw(send_command_ activate_);

my $send_command;
my $read_response;
my $activate;

sub initialize_ {
    my $osname = $^O;
    {
      $ffi = FFI::Platypus->new( api => 1 );
      use FFI::Platypus::DL qw( dlopen dlerror RTLD_PLATYPUS_DEFAULT );
      my $dir = File::Spec->rel2abs( __FILE__ );
      my $current_dir = path($dir)->parent(3);
      my $perl_native_lib;
      if($osname eq "linux") {
          $perl_native_lib = 'Binaries/Native/Linux/X64/libJavonetPerlRuntimeNative.so';
      }
      elsif($osname eq "darwin") {
          $perl_native_lib = 'Binaries/Native/MacOs/X64/libJavonetPerlRuntimeNative.dylib';
      }
      else {
          $perl_native_lib = 'Binaries/Native/Windows/X64/JavonetPerlRuntimeNative.dll';
      }
      $ffi->lib("$current_dir/$perl_native_lib");
      $send_command = $ffi->function('SendCommand' => ['uchar[]', 'int'] => 'int');
      $read_response = $ffi->function('ReadResponse' => ['uchar[]', 'int'] => 'int');
      $activate = $ffi->function('Activate' => ['string', 'string', 'string', 'string', 'string'] => 'int');
    }
}

sub send_command_ {
    my($self, $message_ref) = @_;
    my @message_array = @$message_ref;
    my $response_array_len = $send_command->(\@message_array, scalar @message_array);

    if($response_array_len > 0)
    {
        my @response_array = (1 .. $response_array_len);
        $read_response->(\@response_array, $response_array_len);
        return @response_array;
    } else {
        die "Javonet error code: $response_array_len";
    }
}

sub activate_ {
    my($self, $email, $licenceKey, $proxyHost, $proxyUserName, $proxyPassword) = @_;
    initialize_();
    return $activate->($email, $licenceKey, $proxyHost, $proxyUserName, $proxyPassword);
}

1;
