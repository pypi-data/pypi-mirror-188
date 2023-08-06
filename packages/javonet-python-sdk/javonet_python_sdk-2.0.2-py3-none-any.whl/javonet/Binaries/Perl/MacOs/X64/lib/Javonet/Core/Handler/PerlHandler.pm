package Javonet::Core::Handler::PerlHandler;
use strict;
use warnings FATAL => 'all';
use Moose;
use lib 'lib';
use aliased 'Javonet::Core::Handler::CommandHandler::LoadLibraryHandler' => 'LoadLibraryHandler';
use aliased 'Javonet::Core::Handler::CommandHandler::GetStaticFieldHandler' => 'GetStaticFieldHandler';
use aliased 'Javonet::Core::Handler::CommandHandler::SetStaticFieldHandler' => 'SetStaticFieldHandler';
use aliased 'Javonet::Core::Handler::CommandHandler::CreateClassInstanceHandler' => 'CreateInstanceHandler';
use aliased 'Javonet::Core::Handler::CommandHandler::InvokeInstanceMethodHandler' => 'InvokeInstanceMethodHandler';
use aliased 'Javonet::Core::Handler::CommandHandler::InvokeStaticMethodHandler' => 'InvokeStaticMethodHandler';
use aliased 'Javonet::Core::Handler::CommandHandler::ResolveInstanceHandler' => 'ResolveInstanceHandler';
use aliased 'Javonet::Core::Handler::CommandHandler::GetTypeHandler' => 'GetTypeHandler';
use aliased 'Javonet::Core::Handler::Exception' => 'Exception';
use aliased 'Javonet::Core::Handler::CommandHandler::CastingHandler' => 'CastingHandler';
use aliased 'Javonet::Core::Handler::CommandHandler::GetInstanceFieldHandler' => 'GetInstanceFieldHandler';
use aliased 'Javonet::Core::Handler::CommandHandler::DestructReferenceHandler' => 'DestructReferenceHandler';

use aliased 'Javonet::Sdk::Core::PerlCommandType' => 'PerlCommandType', qw(get_command_type);
use aliased 'Javonet::Sdk::Core::PerlCommand' => 'PerlCommand';
use aliased 'Javonet::Core::Handler::ReferencesCache' => 'ReferencesCache';
use aliased 'Javonet::Core::Handler::AbstractHandler' => 'AbstractHandler';
use aliased 'Javonet::Sdk::Core::RuntimeLib' => 'RuntimeLib', qw(get_runtime);
use aliased 'Javonet::Core::Handler::HandlerDictionary' => 'HandlerDictionary', qw(get_handler);


my $load_library_handler = LoadLibraryHandler->new();
my $get_static_field_handler = GetStaticFieldHandler->new();
my $set_static_field_handler= SetStaticFieldHandler->new();
my $create_instance_handler= CreateInstanceHandler->new();
my $invoke_instance_method_handler = InvokeInstanceMethodHandler->new();
my $invoke_static_method_handler = InvokeStaticMethodHandler->new();
my $resolve_instance_handler = ResolveInstanceHandler->new();
my $get_type_handler = GetTypeHandler->new();
my $casting_handler = CastingHandler->new();
my $get_instance_field_handler = GetInstanceFieldHandler->new();
my $destruct_reference_handler = DestructReferenceHandler->new();


Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('LoadLibrary'),
    $load_library_handler
);
Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('GetStaticField'),
    $get_static_field_handler
);
Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('SetStaticField'),
    $set_static_field_handler
);
Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('CreateClassInstance'),
    $create_instance_handler
);
Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('InvokeInstanceMethod'),
    $invoke_instance_method_handler
);
Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('InvokeStaticMethod'),
    $invoke_static_method_handler
);
Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('Reference'),
    $resolve_instance_handler
);
Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('GetType'),
    $get_type_handler
);
Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('Cast'),
    $casting_handler
);
Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('GetInstanceField'),
    $get_instance_field_handler
);
Javonet::Core::Handler::HandlerDictionary::add_handler_to_dict(
    Javonet::Sdk::Core::PerlCommandType::get_command_type('DestructReference'),
    $destruct_reference_handler
);

sub handle_command {
    my ($self, $command) = @_;
    my $response = Javonet::Core::Handler::HandlerDictionary::get_handler($command->{command_type})->handle_command($command);
    my $reference_cache = ReferencesCache->new();

    if ($response->isa("Javonet::Core::Handler::Exception")){
        return PerlCommand->new(
            runtime => Javonet::Sdk::Core::RuntimeLib::get_runtime('Perl'),
            command_type => Javonet::Sdk::Core::PerlCommandType::get_command_type('Exception'),
            payload => [$response->get_message()]
        )
    }
    if (!blessed($response)){
        return PerlCommand->new(
            runtime => Javonet::Sdk::Core::RuntimeLib::get_runtime('Perl'),
            command_type => Javonet::Sdk::Core::PerlCommandType::get_command_type('Response'),
            payload => [$response]
        )
    }
    else{
        my $guid = $reference_cache->cache_reference($response);
        return PerlCommand->new(
            runtime => Javonet::Sdk::Core::RuntimeLib::get_runtime('Perl'),
            command_type =>  Javonet::Sdk::Core::PerlCommandType::get_command_type('Reference'),
            payload =>  [$guid]
        )
    }
}

no Moose;
1;
