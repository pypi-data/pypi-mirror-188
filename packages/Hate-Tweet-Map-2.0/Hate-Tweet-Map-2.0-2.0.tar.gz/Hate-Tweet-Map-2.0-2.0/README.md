# Hate-Tweet-Map-2.0
Estensione del già esistente tool _Hate Tweet Map_.
Le estensioni apportate comprendono i seguenti parametri presenti nel file di configurazione <code>search_tweets.config</code>:
# Campo user_mentioned
Aggiunta del campo _user_mentioned_ nel file di configurazione <code>search_tweets.config </code> utilizzando sia l’attributo __to:__ che l’attributo __@__:

• Utilizzando l’attributo to: nella creazione della query, si ottengono tutti i tweet che includono la menzione di particolari account sotto forma di risposta. Ad esempio,     si vogliono trovare tutti i tweet in cui l’utente A è stato menzionato; con l’attributo to: saranno trovati tutti i tweet che hanno RISPOSTO a un tweet pubblicato             dall’utente A.
    
• Utilizzando l’attributo @ nella creazione della query, si ottengono tutti i tweet che includono la menzione di particolari account sia sotto forma di risposta, sia sotto     forma di retweet e sia sotto forma di quoted. Ad esempio, si vogliono trovare tutti i tweet in cui l’utente A è stato menzionato; con l’attributo @ saranno trovati tutti i     tweet di account che hanno risposto a un tweet dell’utente A o che hanno ritwittato un tweet dell’utente A o che hanno semplicemente menzionato in un loro tweet.

# Campo hashtag
Aggiunta del campo _hashtag_ nel file di configurazione search_tweets.config utilizzando l’attributo __#__: 

Questo operatore trova la corrispondenza con qualsiasi tweet che contenga un hashtag. Inoltre, esegue una corrispondenza esatta, NON una corrispondenza tokenizzata, il che significa che all’hashtag #covid corrisponderanno i post con l'hashtag esatto #covid, ma non quelli con l'hashtag #covid19

# Campo has:images
Aggiunta del campo _has:images_ nel file di configurazione search_tweets.config utilizzando l’attributo __has:images__ :

Questo attributo trova i tweet che contengo un URL di un’immagine. Ad esempio, inserendo nel file di configurazione l’hashtag #covid e settando a True il parametro has:images, si otterranno tutti i tweet con quel particolare hashtag e che contengono un’immagine.

# Modifica parametro processed
Aggiunta di nuovi attributi utili per migliorare il funzionamento del parametro _processed_.
Il parametro _processed_ può avere due valori _(True/False)_ ed è utile per quanto riguarda l’altro parametro _analyze_all_tweets_, presente nel file di configurazione <code>process_tweets.config</code>.

# Creazione script edge_list_converter
Questo script permette di convertire una collection con tutti i tweet estratti, attraverso il file <code>SearchTweets.py</code>, in un file _CSV_ nel formato corretto per essere importato all'interno del software di Social Network Analysis __Gephi__. 

Dato che Gephi permette di importare una lista di archi solo se sono presenti i due campi _Source_ e _Target_, attraverso l'utilizzo del file di configurazione <code>edge_list_script.config</code>, è possibile inserire l'attributo che si vuole avere come _Source_ e l'attributo che si vuole avere come _Target_.

E' possibile creare i seguenti archi:

• __Utente-->UTILIZZA-->Hashtag:__
Per creare questo arco, si dovranno inserire nel file di configurazione <code>edge_list_script.config</code> i seguenti dati:
    
 -<code>Source</code>: author_username
 
 -<code>Target</code>: hashtag
 
 • __Utente-->RETWEET-->Utente:__
Per creare questo arco, si dovranno inserire nel file di configurazione <code>edge_list_script.config</code> i seguenti dati:
    
 -<code>Source</code>: author_username
 
 -<code>Target</code>: user_retweeted
 
 • __Utente-->MENZIONA-->Utente:__
Per creare questo arco, si dovranno inserire nel file di configurazione <code>edge_list_script.config</code> i seguenti dati:
    
 -<code>Source</code>: author_username
 
 -<code>Target</code>: user_mentioned
 
  • __Hashtag-->UTILIZZATO NEL CONTESTO DI-->Utente menzionato:__
Per creare questo arco, si dovranno inserire nel file di configurazione <code>edge_list_script.config</code> i seguenti dati:
    
 -<code>Source</code>: hashtag
 
 -<code>Target</code>: user_mentioned
