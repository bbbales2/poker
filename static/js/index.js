var Index = Index || {}

Index.Controller = Backbone.View.extend(
    {
        events : {
            "change .hide" : "drawCards"
        },

        initialize : function(options)
        {
        },

        drawCards : function()
        {
            var template = _.template($( '.cardTemplate' ).text());

            $( '.handCards' ).empty();
            $( '.holeCards' ).empty();
            $( '.computerCards' ).empty();
            $( '.computerCards' ).show();
            $( '.winContainer' ).show();

            $( '.bets' ).text( this.data.bets );
            $( '.percent' ).text( this.data.percent );

            var bets = this.data.bets.split('/');
            bets = bets[bets.length - 1];

            var raises = 0;

            if(bets.length > 0)
            {
                for(var i = 0; i < bets.length; i++)
                    if(bets[i] == 'r')
                        raises += 1

                raises -= 1
            }
    
            var goesfirst = (this.data['player'] == 1 && this.data['round'] == 0) || (this.data['player'] == 0 && this.data['round'] > 0)

            $( '.fold' ).prop('disabled', false);
            $( '.check' ).prop('disabled', false);
            $( '.raise' ).prop('disabled', false);

            $( '.playerWallet' ).text( '$' + this.data['wallet']['player'] );
            $( '.computerWallet' ).text( '$' + this.data['wallet']['computer'] );
            $( '.playerPool' ).text( '$' + this.data['pool']['player'] );
            $( '.computerPool' ).text( '$' + this.data['pool']['computer'] );

            if(!goesfirst && bets.length == 1 && bets[0] == 'c')
            {
                $( '.fold' ).prop('disabled', true);
            }
            else if(raises >= 3)
            {
                $( '.raise' ).prop('disabled', true);
            }

            if(this.data.winner == this.data.player)
            {
                $( '.winner' ).text( 'Person won!' );
            }
            else if(this.data.winner == 1 - this.data.player)
            {
                $( '.winner' ).text( 'Computer won!' );
            }
            else if(this.data.winner == 2)
            {
                $( '.winner' ).text( 'Players tied!!!!!' );
            }
            else
            {
                if($( '.hide' ).prop('checked'))
                {
                    $( '.computerCards' ).hide();
                }

                $( '.winContainer' ).hide();
            }

            var rankToString = { 2 : '2',
                                 3 : '3',
                                 4 : '4',
                                 5 : '5',
                                 6 : '6',
                                 7 : '7',
                                 8 : '8',
                                 9 : '9',
                                 T : '10',
                                 J : 'jack',
                                 Q : 'queen',
                                 K : 'king',
                                 A : 'ace' };
            
            var suitToString = { s : 'spades',
                                 d : 'diamonds',
                                 c : 'clubs',
                                 h : 'hearts' };

            for(var i = 0; i < this.data.hcards.length; i++)
            {
                var card = this.data.hcards[i];

                var url = 'static/images/';

                url += rankToString[card[0]] + '_of_' + suitToString[card[1]];

                if(card[0] == 'J' || card[0] == 'Q' || card[0] == 'K')
                    url += '2';

                url += '.png';

                $( template({ url : url }) ).appendTo( $( '.handCards' ) );
            }

            for(var i = 0; i < this.data.ccards.length; i++)
            {
                var card = this.data.ccards[i];

                var url = 'static/images/';

                url += rankToString[card[0]] + '_of_' + suitToString[card[1]];

                if(card[0] == 'J' || card[0] == 'Q' || card[0] == 'K')
                    url += '2';

                url += '.png';

                $( template({ url : url }) ).appendTo( $( '.computerCards' ) );
            }

            for(var i = 0; i < this.data.cards.length; i++)
            {
                var card = this.data.cards[i];

                var url = 'static/images/';

                url += rankToString[card[0]] + '_of_' + suitToString[card[1]];

                if(card[0] == 'J' || card[0] == 'Q' || card[0] == 'K')
                    url += '2';

                url += '.png';

                $( template({ url : url }) ).appendTo( $( '.holeCards' ) );
            }
        },
        
        betFailed : function()
        {
            this.$el.find( '.msg' ).text('Bet failed, try again later');
        },

        do_action : function(play)
        {
            $.ajax( {
                url : '/play',
                data : { action : play },
                dataType : 'json',
                method : 'GET',
                success : _.bind(this.action_result, this)
            } );
        },

        action_result : function(data)
        {
            this.data = data.state;

            this.drawCards();
        },

        render : function()
        {
            this.$el = $("body");
            this.el = this.$el[0];

            this.data = $.parseJSON(this.$el.find( '.data' ).text());

            $( '.raise' ).click(_.bind(_.partial(this.do_action, 'r'), this));
            $( '.check' ).click(_.bind(_.partial(this.do_action, 'c'), this));
            $( '.fold' ).click(_.bind(_.partial(this.do_action, 'f'), this));

            this.drawCards();

            this.delegateEvents();
        },
    }
);

$( document ).ready( function() {
    var cont = new Index.Controller();
    
    cont.render();
});

