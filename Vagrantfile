Vagrant.configure("2") do |config|
    config.vm.box = "generic/ubuntu1604"
    
    config.vm.provider "virtualbox" do |v|
        v.memory = 256
        v.cpus = 1
        v.customize ["modifyvm", :id, "--uartmode1", "disconnected"]
    end

    config.vm.synced_folder ".", "/vagrant", disabled: true
    
    ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
    config.ssh.insert_key = false
    config.vm.provision 'shell', inline: 'rm -rf /root/.ssh'
    config.vm.provision 'shell', inline: 'mkdir -p /root/.ssh'
    config.vm.provision 'shell',
        inline: "echo #{ssh_pub_key} >> /root/.ssh/authorized_keys"
    config.vm.provision 'shell',
        inline: "echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys",
        privileged: false

    config.vm.define "app" do |app|
        app.vm.network "private_network", ip: "10.60.25.10"
        app.vm.hostname = "unvdjangoapp"
        app.vm.provider "virtualbox" do |v|
            v.name = 'unv_django_web_app'
        end
    end
end
