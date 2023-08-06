package Javonet::Core::Handler::CommandHandler::LoadLibraryHandler;
use aliased 'Javonet::Core::Handler::PerlHandler' => 'PerlHandler';
use strict;
use warnings FATAL => 'all';
use Moose;
use lib 'lib';
use Module::Load;
use Nice::Try;
use aliased 'Javonet::Core::Handler::Exception' => 'Exception';
extends 'Javonet::Core::Handler::CommandHandler::AbstractCommandHandler';

sub new {
    my $class = shift;
    my $self = {
        required_parameters_count  => 2
    };
    return bless $self, $class;
}

sub process {
    my ($self, $command) = @_;
    try {
        my $current_payload_ref = $command->{payload};
        my @cur_payload = @$current_payload_ref;
        my $parameters_length = @cur_payload;
        if ($parameters_length != $self->{required_parameters_count}){
            die Exception->new("Exception: LoadLibrary parameters mismatch");
        }
        my $path_to_class = $command->{payload}[0];
        my $class_file = $command->{payload}[1];

        push (@INC,"$path_to_class");
        eval(require $class_file);
        return 0;
    }
    catch ( $e ) {
        return $e ;
    }
}

no Moose;
1;
