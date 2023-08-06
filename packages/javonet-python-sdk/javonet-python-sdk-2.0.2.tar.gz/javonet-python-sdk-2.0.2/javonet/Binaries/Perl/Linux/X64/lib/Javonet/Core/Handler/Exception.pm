package Javonet::Core::Handler::Exception;
use strict;
use warnings FATAL => 'all';
use Moose;
use lib 'lib';

my $message;



sub new {
    my ($proto,$exception_message) = @_;
    my $self = bless {}, $proto;
    $message = $exception_message;
    return $self;
}

sub get_message(){
    my $self = @_;
    return $message;
}

1;