/*
 * ZeroTier One - Network Virtualization Everywhere
 * Copyright (C) 2011-2016  ZeroTier, Inc.  https://www.zerotier.com/
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * This utility makes the World from the configuration specified below.
 * It probably won't be much use to anyone outside ZeroTier, Inc. except
 * for testing and experimentation purposes.
 *
 * If you want to make your own World you must edit this file.
 *
 * When run, it expects two files in the current directory:
 *
 * previous.c25519 - key pair to sign this world (key from previous world)
 * current.c25519 - key pair whose public key should be embedded in this world
 *
 * If these files do not exist, they are both created with the same key pair
 * and a self-signed initial World is born.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include <string>
#include <vector>
#include <algorithm>

#include <node/Constants.hpp>
#include <node/World.hpp>
#include <node/C25519.hpp>
#include <node/Identity.hpp>
#include <node/InetAddress.hpp>
#include <osdep/OSUtils.hpp>

using namespace ZeroTier;

class WorldMaker : public World
{
public:
	static inline World make(uint64_t id,uint64_t ts,const C25519::Public &sk,const std::vector<World::Root> &roots,const C25519::Pair &signWith)
	{
		WorldMaker w;
		w._id = id;
		w._ts = ts;
		w._updateSigningKey = sk;
		w._roots = roots;

		Buffer<ZT_WORLD_MAX_SERIALIZED_LENGTH> tmp;
		w.serialize(tmp,true);
		w._signature = C25519::sign(signWith,tmp.data(),tmp.size());

		return w;
	}
};

int main(int argc,char **argv)
{
	std::string previous,current;
	if ((!OSUtils::readFile("previous.c25519",previous))||(!OSUtils::readFile("current.c25519",current))) {
		C25519::Pair np(C25519::generate());
		previous = std::string();
		previous.append((const char *)np.pub.data,ZT_C25519_PUBLIC_KEY_LEN);
		previous.append((const char *)np.priv.data,ZT_C25519_PRIVATE_KEY_LEN);
		current = previous;
		OSUtils::writeFile("previous.c25519",previous);
		OSUtils::writeFile("current.c25519",current);
		fprintf(stderr,"INFO: created initial world keys: previous.c25519 and current.c25519 (both initially the same)"ZT_EOL_S);
	}

	if ((previous.length() != (ZT_C25519_PUBLIC_KEY_LEN + ZT_C25519_PRIVATE_KEY_LEN))||(current.length() != (ZT_C25519_PUBLIC_KEY_LEN + ZT_C25519_PRIVATE_KEY_LEN))) {
		fprintf(stderr,"FATAL: previous.c25519 or current.c25519 empty or invalid"ZT_EOL_S);
		return 1;
	}
	C25519::Pair previousKP;
	memcpy(previousKP.pub.data,previous.data(),ZT_C25519_PUBLIC_KEY_LEN);
	memcpy(previousKP.priv.data,previous.data() + ZT_C25519_PUBLIC_KEY_LEN,ZT_C25519_PRIVATE_KEY_LEN);
	C25519::Pair currentKP;
	memcpy(currentKP.pub.data,current.data(),ZT_C25519_PUBLIC_KEY_LEN);
	memcpy(currentKP.priv.data,current.data() + ZT_C25519_PUBLIC_KEY_LEN,ZT_C25519_PRIVATE_KEY_LEN);

	// =========================================================================
	// EDIT BELOW HERE

	std::vector<World::Root> roots;

	const uint64_t id = ZT_WORLD_ID_EARTH;
	const uint64_t ts = 1452708876314ULL; // January 13th, 2016

	// Tifa 1
	roots.push_back(World::Root());
    	roots.back().identity = Identity("35b7a18f36:0:e7d0dc4f655c0a2adb72aa9529e97d0fdf1e72bf12a6e753c6b366d88b388b645702edbd8dfeda21c3654f2d73c28fecc7c4713b335ffa61b09e322a7b93c18a");
    	roots.back().stableEndpoints.push_back(InetAddress("103.16.198.213/9993"));

	// Cyber 2
	roots.push_back(World::Root());
    	roots.back().identity = Identity("e4bfc89a12:0:93f764c53030b11c4b9f824cdade6fb731d26b5150f326ca484dbb3acb33a065d5431524fe7ce517512b13c21c4ab5edb04a2e145cefa33ffdf39a855b966c21");
    	roots.back().stableEndpoints.push_back(InetAddress("103.80.237.163/9993"));

    	// Controller Tifa 1 and Cyber 1 as backup
    	roots.push_back(World::Root());
    	roots.back().identity = Identity("9ccd7502d0:0:86de0c08914250d85d1e7c2771dec3ac8f01c9767fd57813854d117e065ac84dfcea576c62e6ed17e3e0d1d81a942936ca2a6c31e534d64e2a4d0a8837a9c6d2");
    	roots.back().stableEndpoints.push_back(InetAddress("103.80.237.27/9993"));
    	roots.back().stableEndpoints.push_back(InetAddress("103.16.198.211/9993"));
    	//roots.back().stableEndpoints.push_back(InetAddress("2a02:6ea0:c815::/9993"));

    	// Ancol
    	roots.push_back(World::Root());
    	roots.back().identity = Identity("117cd947d5:0:8b15bfe3798aa1529abf6def4d4d8eb3ff5cbd50c04ddaf7747adc00a55aef5b6666953ee30a2b6c3c852db7426c42760b7d26c63acdc6489fd11bb36690d966");
    	//roots.back().stableEndpoints.push_back(InetAddress("36.92.72.210/9993"));
    	roots.back().stableEndpoints.push_back(InetAddress("124.158.170.34/9993"));
    	//roots.back().stableEndpoints.push_back(InetAddress("192.168.78.2/9993"));
    	roots.back().stableEndpoints.push_back(InetAddress("123.231.254.50/9993"));
    	//roots.back().stableEndpoints.push_back(InetAddress("2a02:6ea0:c815::/9993"));

	// END WORLD DEFINITION
	// =========================================================================

	fprintf(stderr,"INFO: generating and signing id==%llu ts==%llu"ZT_EOL_S,(unsigned long long)id,(unsigned long long)ts);

	World nw = WorldMaker::make(id,ts,currentKP.pub,roots,previousKP);

	Buffer<ZT_WORLD_MAX_SERIALIZED_LENGTH> outtmp;
	nw.serialize(outtmp,false);
	World testw;
	testw.deserialize(outtmp,0);
	if (testw != nw) {
		fprintf(stderr,"FATAL: serialization test failed!"ZT_EOL_S);
		return 1;
	}

	OSUtils::writeFile("world.bin",std::string((const char *)outtmp.data(),outtmp.size()));
	fprintf(stderr,"INFO: world.bin written with %u bytes of binary world data."ZT_EOL_S,outtmp.size());

	fprintf(stdout,ZT_EOL_S);
	fprintf(stdout,"#define ZT_DEFAULT_WORLD_LENGTH %u"ZT_EOL_S,outtmp.size());
	fprintf(stdout,"static const unsigned char ZT_DEFAULT_WORLD[ZT_DEFAULT_WORLD_LENGTH] = {");
	for(unsigned int i=0;i<outtmp.size();++i) {
		const unsigned char *d = (const unsigned char *)outtmp.data();
		if (i > 0)
			fprintf(stdout,",");
		fprintf(stdout,"0x%.2x",(unsigned int)d[i]);
	}
	fprintf(stdout,"};"ZT_EOL_S);

	return 0;
}
