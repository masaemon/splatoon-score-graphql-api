import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Player as PlayerModel, Score as ScoreModel, db_session

class Player(SQLAlchemyObjectType):
    class Meta:
        model = PlayerModel
        interfaces = (relay.Node, )

class Score(SQLAlchemyObjectType):
    class Meta:
        model = ScoreModel
        interfaces = (relay.Node, )


class InsertScore(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        rule = graphene.String(required=True)
        power = graphene.Int(required=True)
        weapon = graphene.String(required=True)
        result = graphene.String(required=True)

    score = graphene.Field(lambda: Score)

    def mutate(self, info, name, rule, power, weapon, result):
        query = Player.get_query(info)
        player = query.filter(PlayerModel.name == name).first()
        score = ScoreModel(rule=rule, power=power, weapon=weapon, result=result, player=player)
        db_session.add(score)
        db_session.commit()
        return InsertScore(score=score)

class InsertPlayer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    player = graphene.Field(lambda: Player)

    def mutate(self, into, name):
        player = PlayerModel(name=name)
        db_session.add(player)
        db_session.commit()
        return InsertPlayer(player=player)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    player = graphene.Field(lambda: Player, name=graphene.String())
    all_player = SQLAlchemyConnectionField(Player)
    all_score = SQLAlchemyConnectionField(Score, sort=None)

    def resolve_player(self, info, name):
        query = Player.get_query(info)
        result = query.filter(PlayerModel.name == name).first()
        return result

class Mutation(graphene.ObjectType):
    insert_player = InsertPlayer.Field()
    insert_score = InsertScore.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
