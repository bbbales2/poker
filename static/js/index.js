var Index = Index || {}

Index.Controller = Backbone.View.extend(
    {
        events : {
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

            $( '.bets' ).text( this.data.bets );
            $( '.percent' ).text( this.data.percent );

            if(this.data.winner == 0)
            {
                $( '.winner' ).text( 'Person won!' );
            }
            else if(this.data.winner == 1)
            {
                $( '.winner' ).text( 'Computer won!' );
            }
            else if(this.data.winner == 2)
            {
                $( '.winner' ).text( 'Players tied!!!!!' );
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

