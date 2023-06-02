---
title: "ssh"
subtitle: "Notes"
tags: [tools]

date: 2022-02-28
featured: false
draft: true

reading_time: false
profile: false
commentable: true
summary: " "

---


## Create public key for locally saved private key

- My private keys are stored in `~/.ssh/keyname.pem`.

- To create private keys, use `ssh-keygen -y -f path-to-pem-file`.

- For usage example, see
  [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#retrieving-the-public-key)

# Mounting server on my mac

I want to mount `home/fgu/dev/remote` (which I'm gonna call `aws_remote` from my virtual machine onto
`Users/fgu/dev/remote` (`mac_remote`) on my mac. I can do this like so:

```shell
sshfs fgu@$te_ip:$te_remote $mac_remote -o identityfile=$mac_pem'
```

What happens here:
- `mac_pem` contains the private key for a ssh keypair that was generated on
    my AWS virtual machine. So, in this exchange, 
