package Alien::FFI::Install::Files;
use strict;
use warnings;
require Alien::FFI;
sub Inline { shift; Alien::FFI->Inline(@_) }
1;

=begin Pod::Coverage

  Inline

=cut
