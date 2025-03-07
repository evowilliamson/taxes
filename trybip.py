

from bip_utils import Bip84, Bip84Coins, Bip44Changes

# Replace with your zpub
zpub = "zpub6ryDj3umfUZ5VfeXhw2wVVbukRnuS7merX6ppYfZ6yxfzqC4y8xtR9dXgfSxQd8ViY6i524xLf6GC8r4Fqkzfmm6qFXph4VSvxX782bh3wQ"

# Initialize the Bip84 object for Bitcoin
bip84 = Bip84.FromExtendedKey(zpub, Bip84Coins.BITCOIN)

# Define gap limit for address derivation
GAP_LIMIT = 20

# Derive Receiving (External) Addresses: m/84'/0'/0'/0/i
print("Receiving Addresses (m/84'/0'/0'/0/i):")
for i in range(GAP_LIMIT):
    addr = bip84.Change(Bip44Changes.CHAIN_EXT).AddressIndex(i).PublicKey().ToAddress()
    print(f"Path: m/84'/0'/0'/0/{i}, Address: {addr}")

# Derive Change (Internal) Addresses: m/84'/0'/0'/1/i
print("\nChange Addresses (m/84'/0'/0'/1/i):")
for i in range(GAP_LIMIT):
    addr = bip84.Change(Bip44Changes.CHAIN_INT).AddressIndex(i).PublicKey().ToAddress()
    print(f"Path: m/84'/0'/0'/1/{i}, Address: {addr}")




""" 

Address: bc1qvplt5nq0emaztuen8swhswv70p050muvxky0e3, Balance at block 833500: 0 satoshis
Address: bc1qnglm37as5jwst05nwfgt3pstraghnllhg52cna, Balance at block 833500: 0 satoshis
Address: bc1q7r9w29nupy0dea7wtcdqnfnwxvke6065kpcphk, Balance at block 833500: 0 satoshis
Address: bc1qz0fj8rj7g9waf8jjzp70z43p2enyf0m9lxhrjl, Balance at block 833500: 0 satoshis
Address: bc1qhqrjn5xkuvq3qmclfrrvf5f43ya0er4gxuq2rp, Balance at block 833500: 0 satoshis
Address: bc1qptyfnrn8x6sr7cfndsfcd9xnetwxfw5x8z2wy3, Balance at block 833500: 0 satoshis
Address: bc1qemulh37en2yd0ts8yas66asudnwc2dagevd9p0, Balance at block 833500: 0 satoshis
Address: bc1q6yxnw2erp5a5pl9rwhhqxzpgl3kg97tv2lfsnd, Balance at block 833500: 0 satoshis
Address: bc1qsefxtuxz3t9qkxh4zlshvlfkhs9tldnxd3dtmy, Balance at block 833500: 0 satoshis
Address: bc1q93tuz4rpmvgljgpk3j6n9wze5mslfq3vtahx73, Balance at block 833500: 0 satoshis
Address: bc1q9wu8xzla83y8fa98nhw9wl0hqdvdxjncsfg0tj, Balance at block 833500: 0 satoshis
Address: bc1qwj7q5j02gtphl29rsdwmrj0knzmm8as9tfc83x, Balance at block 833500: 0 satoshis
Address: bc1qpjxwkxze3wrcy096m8d39vf93gerdkz4l9pcrq, Balance at block 833500: 0 satoshis
Address: bc1qry235cjkm28nkzu0qp0986r42jgym6p48jk72k, Balance at block 833500: 0 satoshis
Address: bc1qk539fhxrk22pr3trqsshglqelsc3avh9a37gc8, Balance at block 833500: 0 satoshis
Address: bc1qte37pt7trc6f9ph9l5d6xk8fjfn3wyk8duf39z, Balance at block 833500: 0 satoshis
Address: bc1qcjvd0r462kxjjvc3xfne8q298mjmcr8cqmku8l, Balance at block 833500: 0 satoshis
Address: bc1ql9vap9mha6c0aayxfrc0w7j2ssqdkz28hjkjwx, Balance at block 833500: 0 satoshis
Address: bc1q38435aqm92mj9kye7zp0fy4h3n6p03jtg2pesn, Balance at block 833500: 0 satoshis
Address: bc1qvz2u45v382j3m2k3w5t5km2c2xzfutusceml5g, Balance at block 833500: 0 satoshis
Address: bc1q8grc9r5kwtdu7yu5r7ydedgvq2scjhtzru3gvz, Balance at block 833500: 0 satoshis
Address: bc1qt06zh3p6k3sqyj0u5q5mwxam35afcw0099prlt, Balance at block 833500: 0 satoshis
Address: bc1q6x4snfrrtz872z4svmj3gfzxtjtuum9zlcyg0q, Balance at block 833500: 0 satoshis
Address: bc1q7kue7q95uqz35c94wt4hxupazhjjlkqtpuzgks, Balance at block 833500: 0 satoshis
Address: bc1q84vy8c0lxs7juwjja8dkmtjdrz2xurx4rvzpap, Balance at block 833500: 0 satoshis
Address: bc1q7zhueh66am23hpmxuuq3nuvn2rv0u8kk0avkut, Balance at block 833500: 0 satoshis
Address: bc1qayay0mxfft9vpvhduegncpgqa42eecq2ndypdn, Balance at block 833500: 0 satoshis
Address: bc1q6seqkcgwzuh39jz4spvx3zm668z4n3uqgw4y7r, Balance at block 833500: 0 satoshis
Address: bc1qngugtlprc0nlnz3qz35gx2za4k64d7jyw96gka, Balance at block 833500: 0 satoshis
Address: bc1q3u5l8p8sd0m4tps049elgzenydzed7t9ptjtyr, Balance at block 833500: 0 satoshis
Address: bc1qwfda06dl0t70sndl2q8sdf7te53meddtn7upse, Balance at block 833500: 0 satoshis
Address: bc1qv28dvm4tpkwyhmjf0fgntmv4m2679t04ccpuwr, Balance at block 833500: 0 satoshis
Address: bc1q9wunuyxc6cz5gwawns78py6rqvd3k2wl9ayuxu, Balance at block 833500: 0 satoshis
Address: bc1qh20fcanefsuukrycfswyg2dprezsq0swxxucfn, Balance at block 833500: 0 satoshis
Address: bc1qcxdaenkgr3vvafgqf6fdkwp33lcf3cvpj56t8w, Balance at block 833500: 0 satoshis
Address: bc1q2mjga2s05k8p5hr84zdp5xgqejjd7e9006dyfd, Balance at block 833500: 0 satoshis
Address: bc1qpwal4e6yzm6zrzmclpepz55uul4xf2m2t3rw62, Balance at block 833500: 0 satoshis
Address: bc1qq7hq92zl7nzzfr7q3rtw9rskr47gwmj72n40r2, Balance at block 833500: 0 satoshis
Address: bc1qn7t5wzvxlqxg94ydsxx9emycv93xas4pteaj3n, Balance at block 833500: 0 satoshis
Address: bc1qpmzljmmuepz046cuydzvz7unskw92l9yll529k, Balance at block 833500: 0 satoshis



 """