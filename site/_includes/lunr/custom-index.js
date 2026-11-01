// lunr の既定の処理（英語の語幹化・記号の除去）は日本語の語を消してしまうので外す
this.pipeline.reset();
this.searchPipeline.reset();
