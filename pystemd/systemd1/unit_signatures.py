#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#


from pystemd.dbuslib import apply_signature
from pystemd.utils import x2char_star


# This is where we add the units and signatures, we steal most of this from
# https://github.com/systemd/systemd/tree/master/src/core/ any of the dbus-*.c
# has that data.

# This dict should have a key, value, where value should be either a byte (
# the signatute) or a callable that returns a tuple of key, signature, value.
# please note that this is not recursive.

KNOWN_UNIT_SIGNATURES = {
    b"Requires": b"as",
    b"Requisite": b"as",
    b"Wants": b"as",
    b"BindsTo": b"as",
    b"PartOf": b"as",
    b"RequiredBy": b"as",
    b"RequisiteOf": b"as",
    b"WantedBy": b"as",
    b"BoundBy": b"as",
    b"ConsistsOf": b"as",
    b"Conflicts": b"as",
    b"ConflictedBy": b"as",
    b"Before": b"as",
    b"After": b"as",
    b"OnFailure": b"as",
    b"Triggers": b"as",
    b"TriggeredBy": b"as",
    b"PropagatesReloadTo": b"as",
    b"ReloadPropagatedFrom": b"as",
    b"JoinsNamespaceOf": b"as",
    b"RequiresMountsFor": b"as",
    b"Documentation": b"as",
    b"SourcePath": b"s",
    b"StopWhenUnneeded": b"b",
    b"RefuseManualStart": b"b",
    b"RefuseManualStop": b"b",
    b"AllowIsolate": b"b",
    b"DefaultDependencies": b"b",
    b"OnFailureJobMode": b"s",
    b"IgnoreOnIsolate": b"b",
    b"JobTimeoutAction": b"s",
    b"JobTimeoutRebootArgument": b"s",
    b"Conditions": b"a(sbbsi)",
    b"Asserts": b"a(sbbsi)",
    b"FailureAction": b"s",
    b"SuccessAction": b"s",
    b"RebootArgument": b"s",
    b"CollectMode": b"s",
    b"User": b"s",
    b"Type": b"s",
    b"Group": b"s",
    b"Nice": b"i",
    b"DynamicUser": b"b",
    b"Personality": b"s",
    b"Description": b"s",
    b"NotifyAccess": b"s",
    b"BusName": b"s",
    b"RemainAfterExit": b"b",
    b"NoNewPrivileges": b"b",
    b"RootDirectoryStartOnly": b"b",
    b"PermissionsStartOnly": b"b",
    # exec_command
    b"ExecStartPre": b"a(sasb)",
    b"ExecStart": b"a(sasb)",
    b"ExecStartPost": b"a(sasb)",
    b"ExecReload": b"a(sasb)",
    b"ExecStop": b"a(sasb)",
    b"ExecStopPost": b"a(sasb)",
    # execute properties
    b"UtmpIdentifier": b"s",
    b"UtmpMode": b"s",
    b"PAMName": b"s",
    b"SELinuxContext": b"s",
    b"KeyringMode": b"s",
    b"SyslogLevelPrefix": b"b",
    b"MemoryDenyWriteExecute": b"b",
    b"RestrictRealtime": b"b",
    b"RemoveIPC": b"b",
    b"MountAPIVFS": b"b",
    b"CPUSchedulingResetOnFork": b"b",
    b"LockPersonality": b"b",
    b"SupplementaryGroups": b"as",
    b"SystemCallArchitectures": b"as",
    b"SystemCallFilter": b"(bas)",
    # timeouts
    b"RuntimeMaxUSec": b"t",
    b"RuntimeMaxSec": lambda _, value: (b"RuntimeMaxUSec", b"t", int(value * 10 ** 6)),
    b"WatchdogUSec": b"t",
    b"WatchdogSec": lambda _, value: (b"WatchdogUSec", b"t", int(value * 10 ** 6)),
    # syslog
    b"SyslogIdentifier": b"s",
    # stdio signatures
    b"StandardInput": b"s",
    b"StandardOutput": b"s",
    b"StandardError": b"s",
    b"TTYPath": b"s",
    b"TTYReset": b"b",
    b"TTYVHangup": b"b",
    b"TTYVTDisallocate": b"b",
    b"IgnoreSIGPIPE": b"b",
    b"StandardInputFileDescriptor": b"h",
    b"StandardOutputFileDescriptor": b"h",
    b"StandardErrorFileDescriptor": b"h",
    b"StandardInputData": b"ay",
    b"Environment": b"as",
    b"PassEnvironment": b"as",
    b"UnsetEnvironment": b"as",
    b"EnvironmentFiles": b"a(sb)",
    # timer signatures
    b"OnActiveSec": b"t",
    b"RemainAfterElapse": b"b",
    b"OnUnitActiveSec": b"t",
    b"OnCalendar": b"s",
    b"OnStartupSec": b"t",
    b"OnBootSec": b"t",
    b"OnUnitInactiveSec": b"t",
    # paths config
    b"WorkingDirectory": b"s",
    b"RootDirectory": b"s",
    b"RootImage": b"s",
    # binds and paths
    b"BindPaths": b"a(ssbt)",
    b"BindReadOnlyPaths": b"a(ssbt)",
    b"ReadWritePaths": b"as",
    b"ReadOnlyPaths": b"as",
    b"ReadWriteDirectories": b"as",
    b"ReadOnlyDirectories": b"as",
    b"InaccessibleDirectories": b"as",
    b"InaccessiblePaths": b"as",
    b"TemporaryFileSystem": b"a(ss)",
    b"MountFlags": b"t",
    b"StateDirectory": b"as",
    b"CacheDirectory": b"as",
    b"LogsDirectory": b"as",
    b"RuntimeDirectory": b"as",
    b"RuntimeDirectoryPreserve": b"s",
    b"ConfigurationDirectory": b"as",
    b"JoinsNamespaceOf": b"as",
    b"PrivateTmp": b"b",
    b"PrivateDevices": b"b",
    b"PrivateNetwork": b"b",
    b"PrivateUsers": b"b",
    b"ProtectKernelTunables": b"b",
    b"ProtectKernelModules": b"b",
    b"ProtectControlGroups": b"b",
    b"ProtectHome": b"s",
    b"ProtectSystem": b"s",
    # systemd.kill
    b"KillMode": b"s",
    b"KillSignal": b"i",
    b"SendSIGHUP": b"b",
    b"SendSIGKILL": b"b",
    b"RestartPreventExitStatus": b"(aiai)",
    b"RestartForceExitStatus": b"(aiai)",
    b"SuccessExitStatus": b"(aiai)",
    # Limits
    b"LimitCPU": b"t",
    b"LimitCPUSoft": b"t",
    b"LimitFSIZE": b"t",
    b"LimitFSIZESoft": b"t",
    b"LimitDATA": b"t",
    b"LimitDATASoft": b"t",
    b"LimitSTACK": b"t",
    b"LimitSTACKSoft": b"t",
    b"LimitCORE": b"t",
    b"LimitCORESoft": b"t",
    b"LimitRSS": b"t",
    b"LimitRSSSoft": b"t",
    b"LimitNOFILE": b"t",
    b"LimitNOFILESoft": b"t",
    b"LimitAS": b"t",
    b"LimitASSoft": b"t",
    b"LimitNPROC": b"t",
    b"LimitNPROCSoft": b"t",
    b"LimitMEMLOCK": b"t",
    b"LimitMEMLOCKSoft": b"t",
    b"LimitLOCKS": b"t",
    b"LimitLOCKSSoft": b"t",
    b"LimitSIGPENDING": b"t",
    b"LimitSIGPENDINGSoft": b"t",
    b"LimitMSGQUEUE": b"t",
    b"LimitMSGQUEUESoft": b"t",
    b"LimitNICE": b"t",
    b"LimitNICESoft": b"t",
    b"LimitRTPRIO": b"t",
    b"LimitRTPRIOSoft": b"t",
    b"LimitRTTIME": b"t",
    b"LimitRTTIMESoft": b"t",
    # cgroup
    b"DevicePolicy": b"s",
    b"Slice": b"s",
    b"Delegate": b"b",
    b"CPUAccounting": b"b",
    b"MemoryAccounting": b"b",
    b"MemoryLow": b"t",
    b"MemoryLowScale": b"u",
    b"MemoryHigh": b"t",
    b"MemoryHighScale": b"u",
    b"MemoryMax": b"t",
    b"MemoryMaxScale": b"u",
    b"MemorySwapMax": b"t",
    b"MemorySwapMaxScale": b"u",
    b"MemoryLimit": b"t",
    b"MemoryLimitScale": b"u",
    b"IOAccounting": b"b",
    b"BlockIOAccounting": b"b",
    b"TasksAccounting": b"b",
    b"TasksMax": b"t",
    b"TasksMaxScale": b"u",
    b"CPUQuota": lambda _, value: (b"CPUQuotaPerSecUSec", b"t", int(value * 10 ** 6)),
    b"CPUQuotaPerSecUSec": b"t",
    b"IPAccounting": b"b",
    b"IPAddressAllow": b"a(iayu)",
    b"IPAddressDeny": b"a(iayu)",
    b"_custom": lambda _, value: value,
}


def signature_array(properties):
    args = [(ord(b"a"), b"(sv)")]
    for prop_name, prop_value in properties.items():
        prop_name = x2char_star(prop_name)
        signature = KNOWN_UNIT_SIGNATURES[prop_name]

        if callable(signature):
            prop_name, signature, prop_value = signature(prop_name, prop_value)

        args += [(ord(b"r"), b"sv"), (ord(b"s"), prop_name)]
        args += [(ord(b"v"), signature)]
        args += apply_signature(signature, [prop_value])
        args += [(-1, None), (-1, None)]
    args += [(-1, None)]

    return args